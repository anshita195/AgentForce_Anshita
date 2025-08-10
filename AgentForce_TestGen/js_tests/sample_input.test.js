const { calculateFactorial, greet } = require('../examples/sample_input');

describe('calculateFactorial', () => {
  it('should return 1 when n is 0', () => {
    expect(calculateFactorial(0)).toBe(1);
  });
  it('should return -1 when n is negative', () => {
    expect(calculateFactorial(-1)).toBe(-1);
  });
  it('should return the factorial of a positive number', () => {
    expect(calculateFactorial(5)).toBe(120);
  });
  it('should return the factorial of 1', () => {
    expect(calculateFactorial(1)).toBe(1);
  });
});

describe('greet', () => {
  it('should return a greeting with the given name', () => {
    expect(greet('World')).toBe('Hello, World!');
  });
  it('should return a greeting with an empty name', () => {
    expect(greet('')).toBe('Hello, !');
  });
  it('should return a greeting with a numerical name', () => {
    expect(greet(123)).toBe('Hello, 123!');
  });
});
