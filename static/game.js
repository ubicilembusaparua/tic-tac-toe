document.addEventListener("DOMContentLoaded", () => {
  const board = document.querySelector(".board");
  if (!board) {
    return;
  }

  board.classList.add("is-animating");

  const tiles = Array.from(board.querySelectorAll(".square"));
  tiles.forEach((tile, index) => {
    tile.style.animationDelay = `${index * 70}ms`;
  });

  window.setTimeout(() => {
    board.classList.remove("is-animating");
    tiles.forEach((tile) => {
      tile.style.animationDelay = "";
    });
  }, 700);

  if (board.dataset.finished === "true") {
    board.classList.add("is-finished");
  }

  const winningLine = board.dataset.winningLine
    .split(",")
    .map((value) => Number.parseInt(value, 10))
    .filter((value) => Number.isInteger(value));

  if (winningLine.length > 0) {
    winningLine.forEach((index, order) => {
      const tile = board.querySelector(`.square[data-index="${index}"]`);
      if (!tile) {
        return;
      }

      window.setTimeout(() => {
        tile.classList.add("is-winning");
      }, order * 160);
    });
  }
});
