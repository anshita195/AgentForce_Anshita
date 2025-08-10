const { calculateFactorial, greet } = require('../examples/sample_input');

describe('calculateFactorial', () => {
  it('should return 1 for factorial of 0', () => {
    expect(calculateFactorial(0)).toBe(1);
  });
  it('should return 1 for factorial of 1', () => {
    expect(calculateFactorial(1)).toBe(1);
  });
  it('should return 120 for factorial of 5', () => {
    expect(calculateFactorial(5)).toBe(120);
  });
  it('should return -1 for factorial of negative number', () => {
    expect(calculateFactorial(-1)).toBe(-1);
  });
  it('should return 3628800 for factorial of 10', () => {
    expect(calculateFactorial(10)).toBe(3628800);
  });
});

describe('greet', () => {
  it('should greet John correctly', () => {
    expect(greet('John')).toBe(`Hello, John!`);
  });
  it('should greet Jane correctly', () => {
    expect(greet('Jane')).toBe(`Hello, Jane!`);
  });
  it('should greet with an empty string', () => {
    expect(greet('')).toBe(`Hello, !`);
  });
});
