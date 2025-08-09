const { calculateFactorial, greet } = require('../examples/sample_input');

describe('calculateFactorial', () => {
  it('should return 1 for 0', () => {
    expect(calculateFactorial(0)).toBe(1);
  });
  it('should return 1 for 1', () => {
    expect(calculateFactorial(1)).toBe(1);
  });
  it('should return 2 for 2', () => {
    expect(calculateFactorial(2)).toBe(2);
  });
  it('should return 6 for 3', () => {
    expect(calculateFactorial(3)).toBe(6);
  });
  it('should return 24 for 4', () => {
    expect(calculateFactorial(4)).toBe(24);
  });
  it('should return 120 for 5', () => {
    expect(calculateFactorial(5)).toBe(120);
  });
  it('should return -1 for negative numbers', () => {
    expect(calculateFactorial(-1)).toBe(-1);
  });
});

describe('greet', () => {
  it('should greet John correctly', () => {
    expect(greet('John')).toBe("Hello, John!");
  });
  it('should greet Jane correctly', () => {
    expect(greet('Jane')).toBe("Hello, Jane!");
  });
  it('should greet an empty string correctly', () => {
    expect(greet('')).toBe("Hello, !");
  });
});
