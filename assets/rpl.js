#!/usr/bin/env node

var fs = require('fs');
var arg = process.argv.slice(2);

if (arg[0]) {
    try {
        var content = fs.readFileSync(arg[0], 'utf-8');
        content = content.replace(/[^\x00-\xff]/g, function(chinese) {
            return escape(chinese).replace(/%u/g, '\\u');
        });
        fs.writeFileSync(arg[1] || arg[0], content, 'utf-8');
        console.log('transfer ' + arg[0] + ' ok');
    } catch (e) {
        console.log(e);
    }
} else {
    console.log('are you testing me?');
}