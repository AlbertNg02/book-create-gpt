const socket=io('http://127.0.0.1');

socket.on('connect', function () {
    console.log('Connected to server!');
});

socket.on('output_update', function (data) {
    console.log('##########################');
    $('#content').html(data.output);
});


