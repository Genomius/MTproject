/**
 * Created by den on 19.04.15.
 */

function autosize(width) {
        // Успешно ли подключен ВК скрипт
        if (typeof VK.callMethod != 'undefined') {
            VK.callMethod('resizeWindow', 840, document.getElementById('body').clientHeight + 60);
        }
    }
    $(document).ready( function(){
        //Вызываем функцию регулировки высоты каждые пол секунды.
        setInterval('autosize(607)', 500);
    });