# 🐛 BUG: Python Workers can't be compiled under Windows

## Which Cloudflare product(s) does this pertain to?

Workers for Platforms

## What version(s) of the tool(s) are you using?

3.50.0 [Wrangler], 3.10.0 [CPython]

## What version of Node are you using?

20.12.1

## What operating system and version are you using?

Windows 11

## Describe the Bug

### Observed behavior

I used the **worker-python template** from this repository.

When using `npm run build` (or `wrangler dev` or `wrangler deploy` that rely on it), the project don't compile (while on Ubuntu it does). **It seems like it got into an issue about path connecting**.

```log
...
ERROR in ./index.py 1:0-38
Module not found: Error: Can't resolve './__target__index.js' in 'D:\a\worker-py-win-bug-repro\worker-py-win-bug-repro'
resolve './__target__index.js' in 'D:\a\worker-py-win-bug-repro\worker-py-win-bug-repro'
...
```

Also, why I'm not using Python 3.7 taht the template requires? Because transcrypt in this python version can't handle any strings! Output in Ubuntu & Python 3.7 like that:

```log
ERROR in ./__target__/index.js 5:22
Module parse failed: Unexpected token (5:22)
You may need an appropriate loader to handle this file type, currently no loaders are configured to process this file. See https://webpack.js.org/concepts#loaders
| var __name__ = '__main__';
| export var handleRequest = function (request) {
>       return new Response (, dict ([[, dict ([[, ]])]]));
| };
| addEventListener (, (function __lambda__ (event) {
 @ ./index.py 1:0-38 1:0-38
```

### Expected behavior

The build can succeed on Ubuntu with Python 3.10:

```log
> worker-python@1.0.0 build
> webpack -c webpack.config.js

asset main.js 17.9 KiB [emitted] [minimized] (name: main)
orphan modules 62.3 KiB [orphan] 2 modules
./index.py + 2 modules 62.3 KiB [built] [code generated]
webp5.91.0 compiled successfully in 1511 ms
```

Expected behaviour is just to build in Windows with Python 3.10. It's simple.

### Steps to reproduce

A windows environment, and follow the instructions of the commands in template:

```powershell
npx wrangler generate worker-py-win-bug-repro https://github.com/cloudflare/workers-sdk/templates/experimental/worker-python
cd worker-py-win-bug-repro
npm install
python -m virtualenv env
.\env\Scripts\activate
pip install transcrypt
npm run build
```

That's all from template, but if required, that's its `wrangler.toml`:

```toml
name = "worker-python"
main = "dist/main.js"
compatibility_date = "2022-06-03"

[build]
command = "npm run build"
```

My worker code is available [here](https://github.com/YYHEggEgg/worker-py-win-bug-repro). Reliably fails? There's even a GitHub Actions for this!

The Workflow in this repo has a matrix of Windows, Ubuntu and Python 3.7, 3.10. Currently only Ubuntu & 3.10 can build; you can check the latest workflow run or fork and run yourself.

The logs are uploaded as artifacts there; `build.log` contains ANSI escape sequences, so you'd better use `cat build.log` to read it.

## Please provide a link to a minimal reproduction

https://github.com/YYHEggEgg/worker-py-win-bug-repro

## Please provide any relevant error logs

Log on Windows & Python 3.10 (it's the same for Python 3.7):

```log
> worker-python@1.0.0 build
> webpack -c webpack.config.js

assets by status 140 bytes [cached] 1 asset
./index.py 38 bytes [built] [code generated]

ERROR in ./index.py 1:0-38
Module not found: Error: Can't resolve './__target__index.js' in 'D:\a\worker-py-win-bug-repro\worker-py-win-bug-repro'
resolve './__target__index.js' in 'D:\a\worker-py-win-bug-repro\worker-py-win-bug-repro'
  using description file: D:\a\worker-py-win-bug-repro\worker-py-win-bug-repro\package.json (relative path: .)
    Field 'browser' doesn't contain a valid alias configuration
    using description file: D:\a\worker-py-win-bug-repro\worker-py-win-bug-repro\package.json (relative path: ./__target__index.js)
      no extension
        Field 'browser' doesn't contain a valid alias configuration
        D:\a\worker-py-win-bug-repro\worker-py-win-bug-repro\__target__index.js doesn't exist
      .js
        Field 'browser' doesn't contain a valid alias configuration
        D:\a\worker-py-win-bug-repro\worker-py-win-bug-repro\__target__index.js.js doesn't exist
      .json
        Field 'browser' doesn't contain a valid alias configuration
        D:\a\worker-py-win-bug-repro\worker-py-win-bug-repro\__target__index.js.json doesn't exist
      .wasm
        Field 'browser' doesn't contain a valid alias configuration
        D:\a\worker-py-win-bug-repro\worker-py-win-bug-repro\__target__index.js.wasm doesn't exist
      as directory
        D:\a\worker-py-win-bug-repro\worker-py-win-bug-repro\__target__index.js doesn't exist

webpack 5.91.0 compiled with 1 error in 819 ms
```

Log on Ubuntu & Python 3.7 here. Honestly I expect not a fix to this but a Python requirement update.

```log
> worker-python@1.0.0 build
> webpack -c webpack.config.js

assets by status 831 bytes [cached] 1 asset
runtime modules 663 bytes 3 modules
cacheable modules 1.69 KiB
  ./index.py 38 bytes [built] [code generated]
  ./__target__/index.js 1.66 KiB [built] [code generated] [1 error]

ERROR in ./__target__/index.js 5:22
Module parse failed: Unexpected token (5:22)
You may need an appropriate loader to handle this file type, currently no loaders are configured to process this file. See https://webpack.js.org/concepts#loaders
| var __name__ = '__main__';
| export var handleRequest = function (request) {
>       return new Response (, dict ([[, dict ([[, ]])]]));
| };
| addEventListener (, (function __lambda__ (event) {
 @ ./index.py 1:0-38 1:0-38

webpack 5.91.0 compiled with 1 error in 474 ms
```
