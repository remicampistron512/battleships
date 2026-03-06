(function () {
  var app = angular.module('battleshipsApp', []);
  var gridSize = 10;
  var cellSize = 40;

  app.controller('GameController', function ($http) {
    var vm = this;
    vm.statusMessage = 'Press "Start New Game" to begin.';
    vm.playerView = buildEmpty();
    vm.playerBoard = buildEmpty();

    vm.startNewGame = function () {
      $http.post('/api/new-game/').then(function (response) {
        gridSize = response.data.grid_size;
        vm.playerView = buildEmpty();
        vm.playerBoard = buildEmpty();
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
      drawBoard('enemyCanvas', vm.playerView, false);
      drawBoard('playerCanvas', vm.playerBoard, true);
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
          ctx.fillStyle = '#0369a1';
          ctx.fillRect(x, y, cellSize, cellSize);
          ctx.strokeStyle = '#7dd3fc';
          ctx.strokeRect(x, y, cellSize, cellSize);

          var cell = board[row][col];
          if (cell === 'X') {
            drawMarker(ctx, x, y, '#ef4444', 'X');
          } else if (cell === 'O') {
            drawMarker(ctx, x, y, '#f8fafc', '•');
          } else if (cell === 'S' && revealShips) {
            drawMarker(ctx, x, y, '#22c55e', '■');
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
