import { initTabHandler } from './tab_handler.js';
import { initFileUpload } from './file_upload.js';
import { initEmailAnalyzer } from './email_analyzer.js';
import { initCopyHandler } from './copy_handler.js';

document.addEventListener("DOMContentLoaded", function () {
    initTabHandler();
    initFileUpload();
    initEmailAnalyzer();
    initCopyHandler();
});