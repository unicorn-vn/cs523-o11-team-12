const BUFFER_SIZE = 3;
const DELAY_READ_INPUT = 1000;
const DELAY_SORT = 500;
const DELAY_WRITE_BUFFER = 500;
const DELAY_OUTPUT = 1000;

let inputBuffer = [];
let chunk1 = [];
let chunk2 = [];
let output1 = [];
let output2 = [];
let outputBuffer = [];
let final_output = [];
let temp_o1 = [];
let temp_o2 = [];

const fileInput = document.getElementById('fileInput');
const inputBufferTextArea = document.getElementById('inputBuffer');
const chunk1TextArea = document.getElementById('chunk1');
const chunk2TextArea = document.getElementById('chunk2');
const output1TextArea = document.getElementById('output1');
const output2TextArea = document.getElementById('output2');