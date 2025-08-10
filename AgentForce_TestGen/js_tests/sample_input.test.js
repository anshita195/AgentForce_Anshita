const { calculateFactorial, greet } = require('../examples/sample_input');

describe('calculateFactorial', () => {
  it('should return 1 for 0', () => {
    expect(calculateFactorial(0)).toBe(1);
  });
  it('should return 1 for 1', () => {
    expect(calculateFactorial(1)).toBe(1);
  });
  it('should return 120 for 5', () => {
    expect(calculateFactorial(5)).toBe(120);
  });
  it('should return 3628800 for 10', () => {
    expect(calculateFactorial(10)).toBe(3628800);
  });
  it('should return -1 for negative numbers', () => {
    expect(calculateFactorial(-1)).toBe(-1);
  });
  it('should return -1 for -5', () => {
    expect(calculateFactorial(-5)).toBe(-1);
  });
});

describe('greet', () => {
  it('should greet World', () => {
    expect(greet('World')).toBe(`Hello, World!`);
  });
  it('should greet Jest', () => {
    expect(greet('Jest')).toBe(`Hello, Jest!`);
  });
  it('should greet empty string', () => {
    expect(greet('')).toBe(`Hello, !`);
  });
});
