var Options = {};
var Root = document.getElementById("root_boxes");
var Modal = document.getElementById("modal");
days = JSON.parse(days.replace(/&quot;/g,'"'))['days'];
var response = JSON.parse(appointments.replace(/&quot;/g,'"'))['appointments'];

// Sample
// var response = [{
//         day: 1,
//         time: 14,
//         owner: "Ahmet Murat"
//     }
// ];



window.onclick = function(event) {
    if (event.target == Modal) {
        Modal.style.display = "none";
    }
};

function getMonday(d) {
  d = new Date(d);
  var day = d.getDay(),
      diff = d.getDate() - day + (day == 0 ? -6:1); // adjust when day is sunday
  return new Date(d.setDate(diff));
}


initCallender(new Date());
reserveItems();

$('#datepicker').datepicker();

function initCallender(d) {

    var turkish_days = ['Pazar','Pazartesi','Salı','Çarşamba','Perşembe','Cuma','Cumartesi'];
    var turkish_months = ['Ocak','Şubat','Mart','Nisan','Mayıs','Haziran','Temmuz','Ağustos','Eylül','Ekim','Kasım','Aralık'];
    var monday = getMonday(d);


    Options.dayDescriptions = [];
    var temp_date = monday;
    for(i = 0; i<7; i++){
        // Options.dayDescriptions.push( (monday.getDate()+i) + ' ' + turkish_months[monday.getMonth()] + ' ' +
        //                              turkish_days[monday.getDay() + i])
        Options.dayDescriptions.push( (monday.getDate()) + ' ' + turkish_months[monday.getMonth()] + ' ' +
                                     turkish_days[monday.getDay()])
        temp_date.setDate(temp_date.getDate() + 1);
    }


    Options.dayLimits = [{'e': days[0].e , 's': days[0].s}, {'e': days[1].e , 's': days[1].s}, {'e': days[2].e , 's': days[2].s}, {'e': days[3].e , 's': days[3].s}, {'e': days[4].e , 's': days[4].s},
                        {'e': days[5].e , 's': days[5].s}, {'e': days[6].e , 's': days[6].s }];

    Options.dayDurations = 1;
    Options.getMinimum = function() {
        minTime = 24;
        for (i = 0; i < 7; i++) {
            if (minTime > Options.dayLimits[i].s) {
                minTime = Options.dayLimits[i].s
            }
        }
        return minTime;
    };
    Options.minTime = Options.getMinimum();
    for (i = 0; i < 7; i++) {
        CreateDayWithDescriptions(i);
    }

}

function CreateDayWithDescriptions(day) {
    var newDiv = CreateDiv(Root, i * 100 + 50, 50, ["header"])
    var text_day = CreateDiv(newDiv, day * 0, 50, [])
    newDiv.innerText = Options.dayDescriptions[day];
    newDiv.id = "day" + day;
    CreateDay(day, newDiv);
}

function CreateDay(day, dayDiv) {
    for (var i = Options.dayLimits[day].s; i < Options.dayLimits[day].e; i = i + Options.dayDurations) {
        //var newDiv = CreateDiv(Root, day * 100 + 50, (i - Options.minTime) * 50 + 100, ["box", "empty"]);
        var newDiv = CreateDiv(dayDiv, day * 0, (i - Options.minTime) * 50 + 100, ["box", "empty"]);
        newDiv.id = ConvertTimeToBoxId(day, i);
        newDiv.textContent = "" + ConvertTimeString(i) + " - " + ConvertTimeString(i + Options.dayDurations);
        newDiv.setAttribute("onclick", "Prompt(this);");
    }

}

function CreateDiv(upperElement, posx, posy, classes) {
    var newDiv = document.createElement('div');
    newDiv.style.position = "absolute";
    newDiv.style.left = (posx) + 'px';
    newDiv.style.top = (posy + 5) + 'px';
    classNameString = "";
    for (items in classes) {
        classNameString = classNameString + " " + classes[items];
    }
    newDiv.className = classNameString;
    upperElement.appendChild(newDiv)
    return newDiv;
}

function ConvertTimeString(val) {
    var mins, hour;
    if (val % 1 != 0) {
        mins = "30";
    } else {
        mins = "00";
    }
    if (val < 10) {
        hour = "0" + (val - (val % 1));
    } else {
        hour = "" + (val - (val % 1));
    }
    return (hour + ":" + mins);
}

function ConvertBoxIdToTime(val) {
    _time = val % 24;
    _day = val - _time / 24;
    return ({ day: _day, time: _time });
}

function ConvertTimeToBoxId(day, time) {
    return day * 24 + time;
}
var selected_item = null;

function Prompt(sender) {
    clicked = sender.id;
    Modal.style.display = "block";

    if (IsFull(clicked)!=null) { // If it is not null, it is a expected item that contain names and dates
        item = IsFull(clicked);

        //$('#reserved_note').empty();

        $('#not_reserved').hide();
        $('#reserved').show();
        $('#reserved_name').empty().append('<a href="/courts/appointments/' + item.owner_id + '/">' + item.owner + '</a>' + ' tarafindan rezerve edildi.');
        $('#reserved_date').empty().append(item.date);
        $('#reserved_note').val(item.note);
        if(item.paid!=false) {
            $('#reserved_paid').empty().append(item.paid);
        }
        else if(item.paid==false){
            $('#reserved_paid').empty().append((price-item.deposit) + " TL ödenmeli. ");
            $('#deposit_paid_reserved').empty().append(item.deposit + ' TL ön ödeme alındı.');
        }
        else if(item.deposit == 0.00 && item.paid == false){
            $('#deposit_paid_reserved').empty().append('Hiç ön ödeme alınmadı.');
        }
        $('#reserved .click_id').val(item.id);
    }
    else {
        $('#date_and_time_info').empty();
        var text_day = $("#" + clicked).parent()
                                       .clone()    //clone the element
                                       .children() //select all the children
                                       .remove()   //remove all the children
                                       .end()  //again go back to selected element
                                       .text();
        var text_time = $('#' + clicked).text();
        $('#date_and_time_info').append("Tarih : " + text_day + " Saat: " + text_time);
        $('#not_reserved input[name=phone], #not_reserved input[name=name], #not_reserved textarea').val("");
        $('.deposit').hide();
        $('#paid').prop('checked', false);
        $('#deposit').prop('checked', false);
        $('.paid').hide();
        $('#not_reserved').show();
        $('#reserved').hide();
    }
}

function IsFull(Id) {
    full = null;
    response.forEach(
        function(item) {
            if (Id == ConvertTimeToBoxId(item.day, item.time)) {

                full = item;

            }
        }
    );
    return full;
}

function reserveItems() {
    response.forEach(
        function(item) {
            var box = document.getElementById(ConvertTimeToBoxId(item.day, item.time));
            box.setAttribute("class", "box taken");
        }
    );
};


function ajaxSuccess(data) {
    var box = document.getElementById(ConvertTimeToBoxId(item.day, item.time));
    box.setAttribute("class", "box empty");
    $('.modal').hide();
    console.log('appointment is deleted');
}


$('#ajaxform_make_reservation').submit(function() {
         $('<input />').attr('type', 'hidden')
          .attr('name', "court_id")
          .attr('value', court_id)
          .appendTo('#ajaxform_make_reservation');
         $('<input />').attr('type', 'hidden')
          .attr('name', "day")
          .attr('value', $('#' + clicked).parent()[0].id.split('day')[1])
          .appendTo('#ajaxform_make_reservation');
         $('<input />').attr('type', 'hidden')
          .attr('name', "time")
          .attr('value',$('#' + clicked).text().split('-')[0].split(' ')[0].split(':')[0])
          .appendTo('#ajaxform_make_reservation');
         $('<input />').attr('type', 'hidden')
             .attr('name', 'monday')
             .attr('value', monday_of_week)
             .appendTo('#ajaxform_make_reservation');
        $('#not_reserved').hide();
        $('#reserved').hide();


});

$('#ajaxform_update_appointment').submit(function () {

});

$('#ajaxform_update_appointment').ajaxForm(function(res_response){
    data = res_response.split("callback(")[1];
    data = data.slice(0,-2);
    data = JSON.parse(data);
    if(data.IsSuccess==true){
        $('#reserved_info p').append('Notununuz güncellendi');
        $("#reserved_info p").show();
        setTimeout(function() { $("#reserved_info p").empty(); $("#reserved_info p").hide(); }, 3000);
    }
    else{
        $('#reserved_info p').append('Notununuz güncellenemedi bir hata oluştu.')
        $("#reserved_info p").show();
        setTimeout(function() { $("#reserved_info p").empty(); $("#reserved_info p").hide(); }, 3000);
    }
});




$('#ajaxform_make_reservation').ajaxForm(function(res_response) {

    if(res_response.IsSuccess == true) {
        var box = $('#' + clicked);
        box.attr('class', 'box taken');
        response.push(res_response.item);
        $('.modal').hide();
    }
    else{
        if(res_response.context == 'float') {
           $('#not_reserved').show();
           $("input[name='deposit_value']").after('<p class="bg-warning">Lütfen karakter girmeyiniz. Sayı giriniz örneğin: 35.00 TL  yerine 35.00</p>');
        }
    }
});

$('#deposit').click(function() {

    if($('#deposit').prop('checked')==true && $('#paid').prop('checked')== true){
          $('.paid').hide();
          $('.deposit').show();
          $('#paid').prop('checked', false);
    }
    else if($('#deposit').prop('checked')==false ){
        $('.deposit').hide();
    }
    else if($('#deposit').prop('checked')==true && $('#paid').prop('checked') == false){
        $('.deposit').show();
    }
    else{
        $('.deposit').hide();
    }
});

$('#paid').click(function () {
    if($('#paid').prop('checked')==true) {
        $('.paid').show();
        $('.deposit').hide();
        if($('#deposit').prop('checked') == true){
            $('#deposit').prop('checked', false);
        }
        $('#deposit').prop('readonly', true);
    }
    else{
        $('.paid').hide();
        $('#deposit').prop('readonly', false);
    }
})


$('#cancel').click( function() {
        if(confirm('Rezervasyonu iptal etmek istediğinize emin misini   z?')){
            $.ajax({
                type: 'POST',
                data: { csrfmiddlewaretoken: csrftoken },
                url: 'http://localhost:8000/courts/calendars/' + $('#reserved .click_id').val() + '/',
                success: ajaxSuccess,
                error: console.log('olmadi')
            });
        };

});



$('#rightarrow').click(function () {
            $.ajax({
                type: 'GET',
                url: 'http://localhost:8000/saha/courts/'+ court_id +'/appointments/?direction=next&date=' + monday_of_week ,
                success: refreshWeek,
                error: function(e) {
                      console.log(e);
                }

            });
});

$('#leftarrow').click(function () {
            $.ajax({
                type: 'GET',
                url: 'http://localhost:8000/saha/courts/'+ court_id +'/appointments/?direction=previous&date=' + monday_of_week ,
                success: refreshWeek,
                error: function(e) {
                      console.log(e);
                }

            });
});



function refreshWeek(data) {

    data = data.split("callback(")[1];
    data = data.slice(0,-2);
    data = JSON.parse(data);

    yeni_pazartesi = data.new_monday;
    yeni_pazartesi = yeni_pazartesi.split('-');
    js_yeni_pazartesi = yeni_pazartesi[1] + '/' + yeni_pazartesi[2] + '/' + yeni_pazartesi[0];
    monday_of_week = js_yeni_pazartesi;
    var d = new Date(yeni_pazartesi[0], yeni_pazartesi[1]-1, yeni_pazartesi[2]);
    $('#root_boxes').empty();
    initCallender(d);
    response = data.appointments;
    reserveItems();


}