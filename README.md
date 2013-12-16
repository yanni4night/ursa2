Ursa2
=====
Enhanced version of [ursa](https://github.com/sogou-ufo/ursa) with [JSON Auto Combining](https://github.com/yanni4night/ursa2/wiki/JSON-Auto-Combining) and [Sub Tpl Preview](https://github.com/yanni4night/ursa2/wiki/Sub-Tpl-Preview).

Install
=====
Checkout from [GitHub](https://github.com/yanni4night/ursa2) and run :
    
    $ python setup.py install

or

    $ pip install ursa2

Super permission may be required.

Usage
=====

###initialize project

    $ ursa2 init

###start server
    
     
     $ ursa2 start [port]
     
###build

    $ ursa2 build [target][--compress][--html]


Dependencies
=====
 - Unix
 - Java 1.5+
 - Python 2.x
 - [node](https://github.com/joyent/node)
 - [less](https://github.com/less/less.js)
 - [docopt](https://github.com/docopt/docopt)
 - [jinja2](https://github.com/mitsuhiko/jinja2)
 - [requests](https://github.com/kennethreitz/requests)


Documents
=====
 - [manifest.json](https://github.com/yanni4night/ursa2/wiki/manifest.json)
 - [Ursa2 Specification](https://github.com/yanni4night/ursa2/wiki/Ursa2-Specification)
 - [JSON Auto Combining](https://github.com/yanni4night/ursa2/wiki/JSON-Auto-Combining)
 - [Sub Tpl Preview](https://github.com/yanni4night/ursa2/wiki/Sub-Tpl-Preview).

LICENCE
=====
The MIT License (MIT)

Copyright (c) 2013 YinYong

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
the Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
