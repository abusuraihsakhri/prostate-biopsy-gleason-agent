const assert = require('node:assert/strict');
const {gradeGroup} = require('./grading.js');
for (const [a,b,score,group] of [
    [3,3,6,1],[3,4,7,2],[4,3,7,3],[4,4,8,4],[3,5,8,4],
    [5,3,8,4],[4,5,9,5],[5,4,9,5],[5,5,10,5]
]) {
    const result = gradeGroup(a,b);
    assert.equal(result.gleasonScore,score);
    assert.equal(result.gradeGroup,group);
}
for (const [a,b] of [[1,3],[2,3],[3,6],['3',4],[3.5,4],[null,5]]) {
    assert.throws(() => gradeGroup(a,b));
}
console.log('Browser grading checks passed');
