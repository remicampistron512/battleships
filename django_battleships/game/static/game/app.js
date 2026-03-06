(function () {
  var app = angular.module('battleshipsApp', []);

  app.config(function ($httpProvider) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
  });
  var uiConfigElement = document.getElementById('ui-config');
  var initialConfig = uiConfigElement ? JSON.parse(uiConfigElement.textContent) : {};
  var gridSize = initialConfig.grid_size || 10;
  var boardSize = 420;
  var cellSize = boardSize / gridSize;
  var animationTime = 0;
  var lastTimestamp = 0;
  var animationFrameId = null;
  var colors = {
    water: initialConfig.water_color || '#0369a1',
    gridLine: initialConfig.grid_line_color || '#7dd3fc',
    hit: initialConfig.hit_color || '#ef4444',
    miss: initialConfig.miss_color || '#f8fafc',
    ship: initialConfig.ship_color || '#22c55e',
  };

  app.controller('GameController', function ($http) {
    var vm = this;
    vm.statusMessage = 'Press "Start New Game" to begin.';
    vm.playerView = buildEmpty();
    vm.playerBoard = buildEmpty();
    vm.showResultPopup = false;
    vm.popupTitle = '';
    vm.popupMessage = '';
    vm.isSolverRunning = false;

    vm.startNewGame = function () {
      $http.post('/api/new-game/').then(function (response) {
        gridSize = response.data.grid_size;
        cellSize = boardSize / gridSize;
        colors = {
          water: response.data.ui.water_color,
          gridLine: response.data.ui.grid_line_color,
          hit: response.data.ui.hit_color,
          miss: response.data.ui.miss_color,
          ship: response.data.ui.ship_color,
        };
        vm.playerView = buildEmpty();
        vm.playerBoard = buildEmpty();
        vm.showResultPopup = false;
        vm.popupTitle = '';
        vm.popupMessage = '';
        vm.isSolverRunning = false;
        resizeCanvases();
        vm.statusMessage = 'Game started. Fire at enemy waters.';
        drawBoards();
      });
    };

    vm.handleEnemyClick = function (event) {
      if (isGameOver() || vm.isSolverRunning) {
        return;
      }
      var target = event.target;
      var rect = target.getBoundingClientRect();
      var x = event.clientX - rect.left;
      var y = event.clientY - rect.top;
      var row = Math.floor(y / cellSize);
      var col = Math.floor(x / cellSize);

      fireAt(row, col, false);
    };

    vm.closePopup = function () {
      vm.showResultPopup = false;
    };

    vm.solveGame = function () {
      if (vm.isSolverRunning || isGameOver()) {
        return;
      }
      vm.isSolverRunning = true;
      vm.showResultPopup = false;
      runSolverTurn();
    };

    function runSolverTurn() {
      if (!vm.isSolverRunning || isGameOver()) {
        vm.isSolverRunning = false;
        return;
      }

      var nextTarget = findNextUntargetedCell(vm.playerView);
      if (!nextTarget) {
        vm.isSolverRunning = false;
        vm.statusMessage = 'Solver stopped: no untargeted cells remain.';
        return;
      }

      fireAt(nextTarget.row, nextTarget.col, true);
    }

    function findNextUntargetedCell(board) {
      for (var row = 0; row < gridSize; row += 1) {
        for (var col = 0; col < gridSize; col += 1) {
          if (board[row][col] === '~' || board[row][col] === 'S') {
            return { row: row, col: col };
          }
        }
      }
      return null;
    }

    function isGameOver() {
      return vm.statusMessage.indexOf('won') > -1;
    }

    function fireAt(row, col, fromSolver) {
      $http.post('/api/fire/', { row: row, col: col }).then(
        function (response) {
          vm.playerView = response.data.player_view;
          vm.playerBoard = response.data.player_board;
          if (response.data.status === 'player_won') {
            vm.statusMessage = 'You won!';
            openResultPopup('Victory!', 'You sank all enemy ships.');
          } else if (response.data.status === 'enemy_won') {
            vm.statusMessage = 'Enemy won. Try again!';
            openResultPopup('Defeat', 'Your fleet has been sunk.');
          } else {
            var enemyTurn = response.data.enemy_turn;
            vm.statusMessage =
              'You ' +
              response.data.player_result +
              '. Enemy fired at (' +
              enemyTurn.row +
              ',' +
              enemyTurn.col +
              ') and ' +
              enemyTurn.result +
              '.';
          }
          drawBoards();

          if (fromSolver) {
            if (response.data.status === 'active') {
              window.setTimeout(runSolverTurn, 120);
            } else {
              vm.isSolverRunning = false;
            }
          }
        },
        function (error) {
          vm.statusMessage = error.data.error || 'Unable to fire.';
          if (fromSolver) {
            vm.isSolverRunning = false;
          }
        }
      );
    }

    function openResultPopup(title, message) {
      vm.popupTitle = title;
      vm.popupMessage = message;
      vm.showResultPopup = true;
      vm.isSolverRunning = false;
    }

    function buildEmpty() {
      var result = [];
      for (var r = 0; r < gridSize; r += 1) {
        result.push([]);
        for (var c = 0; c < gridSize; c += 1) {
          result[r].push('~');
        }
      }
      return result;
    }

    function drawBoards() {
      resizeCanvases();
      drawBoard('enemyCanvas', vm.playerView, false, animationTime);
      drawBoard('playerCanvas', vm.playerBoard, true, animationTime + 0.9);
    }

    function resizeCanvases() {
      ['enemyCanvas', 'playerCanvas'].forEach(function (canvasId) {
        var canvas = document.getElementById(canvasId);
        if (!canvas) return;
        canvas.width = boardSize;
        canvas.height = boardSize;
      });
    }

    function drawBoard(canvasId, board, revealShips, timeValue) {
      var canvas = document.getElementById(canvasId);
      if (!canvas) return;
      var ctx = canvas.getContext('2d');
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      drawOceanBackground(ctx, timeValue);
      drawSunRays(ctx, timeValue);

      for (var row = 0; row < gridSize; row += 1) {
        for (var col = 0; col < gridSize; col += 1) {
          var x = col * cellSize;
          var y = row * cellSize;
          drawWaterCell(ctx, row, col, x, y, timeValue);
          ctx.strokeStyle = colors.gridLine;
          ctx.lineWidth = 1;
          ctx.strokeRect(x, y, cellSize, cellSize);

          var cell = board[row][col];
          if (cell === 'X') {
            drawHitMarker(ctx, x, y, timeValue);
          } else if (cell === 'O') {
            drawMissMarker(ctx, x, y, timeValue);
          } else if (cell === 'S' && revealShips) {
            drawShipMarker(ctx, x, y, timeValue);
          }
        }
      }

      drawCausticsOverlay(ctx, timeValue);
      drawEdgeGlow(ctx, timeValue);
    }

    function drawOceanBackground(ctx, timeValue) {
      var gradient = ctx.createLinearGradient(0, 0, boardSize, boardSize);
      gradient.addColorStop(0, shadeHex(colors.water, 42));
      gradient.addColorStop(0.45, shadeHex(colors.water, 18));
      gradient.addColorStop(1, shadeHex(colors.water, -8));
      ctx.fillStyle = gradient;
      ctx.fillRect(0, 0, boardSize, boardSize);

      var shimmer = ctx.createRadialGradient(
        boardSize * (0.15 + 0.02 * Math.sin(timeValue * 0.4)),
        boardSize * 0.1,
        boardSize * 0.02,
        boardSize * 0.3,
        boardSize * 0.2,
        boardSize * 0.65
      );
      shimmer.addColorStop(0, 'rgba(186, 230, 253, 0.2)');
      shimmer.addColorStop(1, 'rgba(186, 230, 253, 0)');
      ctx.fillStyle = shimmer;
      ctx.fillRect(0, 0, boardSize, boardSize);
    }

    function drawSunRays(ctx, timeValue) {
      ctx.save();
      ctx.globalCompositeOperation = 'screen';
      for (var i = 0; i < 6; i += 1) {
        var rayX = boardSize * (0.12 + i * 0.15 + 0.01 * Math.sin(timeValue + i));
        var ray = ctx.createLinearGradient(rayX, 0, rayX + 24, boardSize);
        ray.addColorStop(0, 'rgba(224, 242, 254, 0.14)');
        ray.addColorStop(1, 'rgba(224, 242, 254, 0)');
        ctx.fillStyle = ray;
        ctx.fillRect(rayX - 14, 0, 44, boardSize);
      }
      ctx.restore();
    }

    function drawWaterCell(ctx, row, col, x, y, timeValue) {
      var wave =
        Math.sin((col * 0.7 + timeValue * 1.8)) +
        Math.cos((row * 0.85 - timeValue * 1.4));
      var alpha = 0.08 + (wave + 2) * 0.04;
      var texture = ctx.createLinearGradient(x, y, x + cellSize, y + cellSize);
      texture.addColorStop(0, 'rgba(224, 242, 254,' + alpha.toFixed(3) + ')');
      texture.addColorStop(1, 'rgba(14, 116, 144, 0.02)');
      ctx.fillStyle = texture;
      ctx.fillRect(x, y, cellSize, cellSize);
    }

    function drawCausticsOverlay(ctx, timeValue) {
      ctx.save();
      ctx.globalCompositeOperation = 'screen';
      ctx.strokeStyle = 'rgba(186, 230, 253, 0.15)';
      ctx.lineWidth = 1.1;
      for (var i = 0; i < gridSize + 4; i += 1) {
        ctx.beginPath();
        for (var x = 0; x <= boardSize; x += 10) {
          var y =
            (i * cellSize * 0.55 +
              Math.sin(x * 0.024 + timeValue * 1.5 + i * 0.8) * 5 +
              Math.cos(x * 0.016 - timeValue * 1.1) * 3) %
            boardSize;
          if (x === 0) {
            ctx.moveTo(x, y);
          } else {
            ctx.lineTo(x, y);
          }
        }
        ctx.stroke();
      }
      ctx.restore();
    }

    function drawEdgeGlow(ctx, timeValue) {
      var glow = ctx.createLinearGradient(0, 0, boardSize, boardSize);
      glow.addColorStop(0, 'rgba(125, 211, 252, 0.35)');
      glow.addColorStop(0.5, 'rgba(125, 211, 252, 0.08)');
      glow.addColorStop(1, 'rgba(125, 211, 252, 0.25)');
      ctx.strokeStyle = glow;
      ctx.lineWidth = 2.5 + Math.sin(timeValue * 1.2) * 0.25;
      ctx.strokeRect(1.25, 1.25, boardSize - 2.5, boardSize - 2.5);
    }

    function drawShipMarker(ctx, x, y, timeValue) {
      drawMarker(ctx, x, y, colors.ship, '■', 26, 0.85);
      ctx.save();
      ctx.globalAlpha = 0.22 + 0.07 * Math.sin(timeValue * 2.2);
      ctx.fillStyle = '#dcfce7';
      ctx.fillRect(x + cellSize * 0.2, y + cellSize * 0.2, cellSize * 0.6, cellSize * 0.18);
      ctx.restore();
    }

    function drawMissMarker(ctx, x, y, timeValue) {
      var pulse = 0.9 + 0.06 * Math.sin(timeValue * 3.1 + x * 0.05 + y * 0.03);
      drawMarker(ctx, x, y, colors.miss, '•', 30 * pulse, 0.96);
    }

    function drawHitMarker(ctx, x, y, timeValue) {
      var pulse = 0.84 + 0.18 * Math.sin(timeValue * 6.2 + x * 0.06 + y * 0.04);
      ctx.save();
      ctx.fillStyle = 'rgba(239, 68, 68, 0.26)';
      ctx.beginPath();
      ctx.arc(x + cellSize / 2, y + cellSize / 2, cellSize * pulse * 0.36, 0, Math.PI * 2);
      ctx.fill();
      ctx.restore();
      drawMarker(ctx, x, y, colors.hit, '✕', 26 + pulse * 2, 1);
    }

    function drawMarker(ctx, x, y, color, marker, fontSize, alpha) {
      ctx.save();
      ctx.globalAlpha = alpha || 1;
      ctx.fillStyle = color;
      ctx.font = (fontSize || 28) + 'px Arial';
      ctx.textAlign = 'center';
      ctx.textBaseline = 'middle';
      ctx.shadowColor = 'rgba(15, 23, 42, 0.4)';
      ctx.shadowBlur = 6;
      ctx.fillText(marker, x + cellSize / 2, y + cellSize / 2);
      ctx.restore();
    }

    function shadeHex(hex, amount) {
      var color = hex.replace('#', '');
      if (color.length === 3) {
        color =
          color[0] + color[0] + color[1] + color[1] + color[2] + color[2];
      }
      var num = parseInt(color, 16);
      var r = clampColor((num >> 16) + amount);
      var g = clampColor(((num >> 8) & 0x00ff) + amount);
      var b = clampColor((num & 0x0000ff) + amount);
      return 'rgb(' + r + ',' + g + ',' + b + ')';
    }

    function clampColor(value) {
      return Math.max(0, Math.min(255, Math.round(value)));
    }

    function animate(timestamp) {
      if (!lastTimestamp) {
        lastTimestamp = timestamp;
      }
      var deltaSeconds = (timestamp - lastTimestamp) / 1000;
      lastTimestamp = timestamp;
      animationTime += Math.min(deltaSeconds, 0.05);
      drawBoards();
      animationFrameId = window.requestAnimationFrame(animate);
    }

    if (!animationFrameId) {
      animationFrameId = window.requestAnimationFrame(animate);
    }
  });
})();
