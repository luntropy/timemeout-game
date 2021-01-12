function shuffle(array) {
  const _array = array.slice(0);
  for (var i = 0; i < _array.length - 1; i++) {
    var randomIndex = Math.floor(Math.random() * (i + 1));
    var temp = _array[i];
    _array[i] = _array[randomIndex];
    _array[randomIndex] = temp;
  }
  return _array;
}

export default function initializeDeck() {
  let id = 0;
  const cards = [
    1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20,
  ].reduce((acc, type) => {
    acc.push({
      id: id++,
      type,
    });
    acc.push({
      id: id++,
      type,
    });
    return acc;
  }, []);
  return shuffle(cards);
}
