
//-->Menu
var sideMenu = document.querySelector('#side_menu')
var ul = document.querySelector('#side_menu_ul')

var ul_visible = false

function hide_span(){
    ul_visible = !ul_visible;

    ul.style.width = ul_visible ? '50px' : '0px';
    ul.style.minWidth = ul_visible ? '100%' : '0px';
}

//-->Index
function priorityColor() {
    const taskRows = document.querySelectorAll('.task_row');

    taskRows.forEach(row => {
        const priority = row.querySelector('.task_priority');

        // Use textContent para obter o texto visível dentro da célula
        if (priority.textContent.trim() === '1') {
            priority.style.backgroundColor = 'yellow';
        }else if(priority.textContent.trim() === '2'){
            priority.style.backgroundColor = 'orange';
        }else if(priority.textContent.trim() === '3'){
            priority.style.backgroundColor = 'red';
        }
    });
}

//remaining time
function updateRemainingTime() {
    const taskRows = document.querySelectorAll('.task_row');

    taskRows.forEach(row => {
        const startTimeText = row.querySelector('.task_start').textContent;
        const endTimeText = row.querySelector('.task_ending').textContent;

        // Formatando as datas no formato ISO 8601 (AAAA-MM-DDTHH:MM:SS)
        const startTimeISO = startTimeText.replace(/(\d{2})\/(\d{2})\/(\d{2}) (\d{2}):(\d{2})/, '20$3-$2-$1T$4:$5:00');
        const endTimeISO = endTimeText.replace(/(\d{2})\/(\d{2})\/(\d{2}) (\d{2}):(\d{2})/, '20$3-$2-$1T$4:$5:00');

        // Convertendo as datas formatadas para o formato aceito pelo JavaScript
        const startTime = Date.parse(startTimeISO);
        const endTime = Date.parse(endTimeISO);
        const now = Date.now();

        const remainingTimeCell = row.querySelector('.task_remaining_time');

        if (isNaN(startTime) || isNaN(endTime)) {
            remainingTimeCell.textContent = " ";
        } else if (now < startTime) {
            remainingTimeCell.textContent = "não começou";
        } else if (now > endTime) {
            remainingTimeCell.textContent = "acabou";
        } else {
            const timeRemaining = endTime - now;
            const days = Math.floor(timeRemaining / (1000 * 60 * 60 * 24));
            const hours = Math.floor((timeRemaining % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
            const minutes = Math.floor((timeRemaining % (1000 * 60 * 60)) / (1000 * 60));

            remainingTimeCell.textContent = days + "d " + hours + "h " + minutes + "m ";
        }
    });
}

window.addEventListener('load', function() {
    // Quando o evento 'load' ocorrer, chame a função priorityColor
    priorityColor();
});

updateRemainingTime();

// Atualizar o tempo restante a cada segundo
setInterval(updateRemainingTime, 1000);