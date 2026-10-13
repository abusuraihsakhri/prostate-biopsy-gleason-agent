(function (root, factory) {
    "use strict";
    const api = factory();
    if (typeof module !== "undefined" && module.exports) module.exports = api;
    else root.GleasonGrade = api;
})(typeof globalThis !== "undefined" ? globalThis : this, function () {
    "use strict";
    const groups = Object.freeze({
        "3+3": 1, "3+4": 2, "4+3": 3,
        "4+4": 4, "3+5": 4, "5+3": 4,
        "4+5": 5, "5+4": 5, "5+5": 5
    });
    function gradeGroup(primary, secondary) {
        const key = primary + "+" + secondary;
        if (!Number.isInteger(primary) || !Number.isInteger(secondary) ||
            !Object.prototype.hasOwnProperty.call(groups, key)) {
            throw new RangeError("Both patterns must be integers from 3 to 5.");
        }
        return Object.freeze({
            primaryPattern: primary, secondaryPattern: secondary,
            gleasonScore: primary + secondary, gradeGroup: groups[key]
        });
    }
    return Object.freeze({gradeGroup});
});
