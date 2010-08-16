onmessage = function (event) {
  // Doesn't matter what the message is, just run the worker.
  run(event.data);
};


function run(data) {
  with(Math) {
    var pi;
    var s = 0;
    for (i=0; i<data.num_iter; i++) {
      x = random();
      y = random();
      if (x*x + y*y < 1.0) {
        s++;
      }
    }
    pi = 4.0*s/(data.num_iter);
    postMessage({estimated_pi: pi, num_iter: data.num_iter});
    postMessage('done');
  }
}
