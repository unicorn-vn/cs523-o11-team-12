function handleFileUpload(event) {
    const file = event.target.files[0];
    const reader = new FileReader();

    reader.onload = function (e) {
        const text = e.target.result;
        const numbers = text.trim().split(/\s+/);

        inputBuffer = numbers.map(n => parseInt(n, 10));
        splitChunk();
    };

    reader.readAsText(file);
}

async function externalSort() {
    while (chunk1.length || chunk2.length) {
        if (chunk1.length) {
            await chunkSortAnimation(1, chunk1, output1TextArea);
        }

        if (chunk2.length) {
            await chunkSortAnimation(2, chunk2, output2TextArea);
        }
    }
    inactiveChunkTxt(1);
    inactiveChunkTxt(2);
}

async function swap() {
    chunk1 = [...output1];
    chunk2 = [...output2];
    output1 = [];
    output2 = [];

    output1TextArea.value = '';
    output2TextArea.value = '';
    chunk1TextArea.value = '';
    chunk2TextArea.value = '';

    chunk1.forEach((element, index) => {
        chunk1TextArea.value += '[' + element.join(' ') + '] ';
    })

    chunk2.forEach((element, index) => {
        chunk2TextArea.value += '[' + element.join(' ') + '] ';
    })
}

async function output() {
    temp_o1 = [...output1[0]];
    temp_o2 = [...output2[0]];
    while (temp_o1.length > 0 && temp_o2.length > 0) {
        $("#heap").html('<span id="heap1_' + temp_o1[0] + '">' + temp_o1[0] + '</span>' + ' <span id="heap2_' + temp_o2[0] + '">' + temp_o2[0] + '</span>');
        await sleep(DELAY_STEP);
        if (temp_o1[0] <= temp_o2[0]) {
            await outputToBuffer(1, temp_o1);
        } else {
            await outputToBuffer(2, temp_o2);
        }
    }

    while (temp_o1.length > 0) {
        $("#heap").html('<span id="heap1_' + temp_o1[0] + '">' + temp_o1[0] + '</span>');
        await sleep(DELAY_STEP);
        await outputToBuffer(1, temp_o1);
    }

    while (temp_o2.length > 0) {
        $("#heap").html('<span id="heap2_' + temp_o2[0] + '">' + temp_o2[0] + '</span>');
        await sleep(DELAY_STEP);
        await outputToBuffer(2, temp_o2);
    }

    if (outputBuffer.length > 0) {
        await fromBufferToResult();
    }
}