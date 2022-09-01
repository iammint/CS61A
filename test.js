// f(1)(2)(3)()

function curry(sum = 0) {
  return (num) => {
    if (num === undefined) {
      return sum;
    }

    return curry(sum + num);
  };
}

const f = curry();
console.log(f(1)(2)(3)());

