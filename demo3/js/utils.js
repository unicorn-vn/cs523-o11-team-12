const sleep = ms => new Promise(r => setTimeout(r, ms));

function merge(arr1, arr2) {
    const mergedArray = arr1.concat(arr2);
    return mergedArray.sort((a, b) => a - b);
}

function activeChunkTxt(id) {
    $("#chunk" + id).css('background-color', 'red');
    $("#output" + id).css('background-color', 'orange');
}
function inactiveChunkTxt(id) {
    $("#chunk" + id).css('background-color', 'transparent');
    $("#output" + id).css('background-color', 'transparent');
}