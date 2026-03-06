(function () {
  var app = angular.module('battleshipsApp', []);
  var uiConfigElement = document.getElementById('ui-config');
  var initialConfig = uiConfigElement ? JSON.parse(uiConfigElement.textContent) : {};
  var gridSize = initialConfig.grid_size || 10;
  var boardSize = 420;
  var cellSize = boardSize / gridSize;
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
        resizeCanvases();
        vm.statusMessage = 'Game started. Fire at enemy waters.';
        drawBoards();
      });
    };

    vm.handleEnemyClick = function (event) {
      if (vm.statusMessage.indexOf('won') > -1) {
        return;
      }
      var target = event.target;
      var rect = target.getBoundingClientRect();
      var x = event.clientX - rect.left;
      var y = event.clientY - rect.top;
      var row = Math.floor(y / cellSize);
      var col = Math.floor(x / cellSize);

      $http.post('/api/fire/', { row: row, col: col }).then(
        function (response) {
          vm.playerView = response.data.player_view;
          vm.playerBoard = response.data.player_board;
          if (response.data.status === 'player_won') {
            vm.statusMessage = 'You won!';
          } else if (response.data.status === 'enemy_won') {
            vm.statusMessage = 'Enemy won. Try again!';
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
        },
        function (error) {
          vm.statusMessage = error.data.error || 'Unable to fire.';
        }
      );
    };

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
      drawBoard('enemyCanvas', vm.playerView, false);
      drawBoard('playerCanvas', vm.playerBoard, true);
    }

    function resizeCanvases() {
      ['enemyCanvas', 'playerCanvas'].forEach(function (canvasId) {
        var canvas = document.getElementById(canvasId);
        if (!canvas) return;
        canvas.width = boardSize;
        canvas.height = boardSize;
      });
    }

    function drawBoard(canvasId, board, revealShips) {
      var canvas = document.getElementById(canvasId);
      if (!canvas) return;
      var ctx = canvas.getContext('2d');
      ctx.clearRect(0, 0, canvas.width, canvas.height);

      for (var row = 0; row < gridSize; row += 1) {
        for (var col = 0; col < gridSize; col += 1) {
          var x = col * cellSize;
          var y = row * cellSize;
          ctx.fillStyle = colors.water;
          ctx.fillRect(x, y, cellSize, cellSize);
          ctx.strokeStyle = colors.gridLine;
          ctx.strokeRect(x, y, cellSize, cellSize);

          var cell = board[row][col];
          if (cell === 'X') {
            drawMarker(ctx, x, y, colors.hit, 'X');
          } else if (cell === 'O') {
            drawMarker(ctx, x, y, colors.miss, '•');
          } else if (cell === 'S' && revealShips) {
            drawMarker(ctx, x, y, colors.ship, '■');
          }
        }
      }
    }

    function drawMarker(ctx, x, y, color, marker) {
      ctx.fillStyle = color;
      ctx.font = '28px Arial';
      ctx.textAlign = 'center';
      ctx.textBaseline = 'middle';
      ctx.fillText(marker, x + cellSize / 2, y + cellSize / 2);
    }

    drawBoards();
  });
})();
