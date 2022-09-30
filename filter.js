inlets = 1;
outlets = 1;

var buffered_notes = [];

function list(){
    // will store the arguments from the list 
    buffered_notes.push(Array.from(arguments));
    
}

function bang(){
    // will output the highest velocity and sum of the times
    var time = 0;
    var vel = 0;

    for (var i = 0; i < buffered_notes.length; i++){
        time += buffered_notes[i][1];
        vel = Math.max(vel, buffered_notes[i][0])
    }
    outlet(0, [time, vel])
    buffered_notes = [];
}