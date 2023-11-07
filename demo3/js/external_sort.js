async function splitChunk() {
    let chunkNow = 1;
    let p_chnk = 0;
    inputBuffer.forEach((element, index) => {
        $("#input-demo").append("<span class='num_inp' id='inp_" + index + "'>" + element + ' </span>');
    });
    while (inputBuffer.length) {
        let output1 = inputBuffer.slice(0, BUFFER_SIZE);
        inputBuffer = inputBuffer.slice(BUFFER_SIZE);
        await sleep(DELAY_STEP);
        // Update the text areas with the sorted data
        inputBufferTextArea.value = output1.join(' ');
        if (chunkNow == 1) {
            chunk1TextArea.value += '[' + output1.join(' ') + '] ';
            chunk1.push(output1);
            chunkNow = 2;
        } else {
            chunk2TextArea.value += '[' + output1.join(' ') + '] ';
            chunk2.push(output1);
            chunkNow = 1;
        }

        $('.num_inp').css('background-color', 'transparent');
        $("#inp_" + (p_chnk * BUFFER_SIZE)).css('background-color', 'red');
        $("#inp_" + (p_chnk * BUFFER_SIZE + 1)).css('background-color', 'red');
        p_chnk++;
    }
    inputBufferTextArea.value = ''
}

async function chunkSortAnimation(id, c_arr, txtArea) {
    await activeChunkTxt(id);
    let temp = [...(c_arr[0] || [])];
    let temp2 = [...(c_arr[1] || [])];
    let out_t = merge(temp, temp2);
    if (id == 1) {
        output1.push(out_t);
        chunk1 = chunk1.slice(2);
    } else {
        output2.push(out_t);
        chunk2 = chunk2.slice(2);
    }
    await sleep(DELAY_STEP / 2);
    txtArea.value += '[' + out_t.join(' ') + '] ';
    await sleep(DELAY_STEP / 2);
    await inactiveChunkTxt(id);
}

async function fromBufferToResult() {
    final_output = [...final_output, ...outputBuffer];
    $("#result").html('<span>' + final_output.join(' ') + '</span>');
    outputBuffer = [];
    $("#bufferOutput").val('');
}

async function outputToBuffer(id, temp_o) {
    $("#heap" + id + "_" + temp_o[0]).css('background-color', 'red');
    await sleep(DELAY_STEP);
    outputBuffer.push(temp_o[0]);
    $("#bufferOutput").val(outputBuffer.join(' '));
    await sleep(DELAY_STEP);
    if (outputBuffer.length >= 2)
        await fromBufferToResult();
    $("#heap" + id + "_" + temp_o[0]).remove();
    if (id == 1)
        temp_o1 = temp_o1.slice(1);
    else
        temp_o2 = temp_o2.slice(1);
    await sleep(DELAY_STEP);
}