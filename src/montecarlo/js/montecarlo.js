/* Web Worker implementation.
 *
 * Copyright 2010 Tobias Rodaebel
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

onmessage = function (event) {
  // Run the worker.
  run(event.data);
};


/*
 * The Web Worker function uses a Monte Carlo Integration to esitmate Pi.
 *
 * Note: In order to get the best possible performance from your Web Worker
 * implementation, make sure that you properly declared all used variables.
 * Otherwise garbage collection will have a noteable impact on performance.
 */
function run(data) {
  with(Math) {
    var start, end;
    var i, x, y, z;
    var count = 0;
    var pi;

    start = new Date();

    for (i=0; i<data.num_iter; i++) {
      x = random();
      y = random();
      z = x*x+y*y;
      if (z < 1.0) count++;
    }

    pi = 4.0*count/(data.num_iter);

    end = new Date();

    postMessage({estimated_pi: pi,
                 num_iter: data.num_iter,
                 duration_ms: end.valueOf()-start.valueOf()});
    postMessage('done');
  }
}
