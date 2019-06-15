# Static Code Analyzer on the web

This site has been built using Vue.js for frontend and Django for backend.

Make sure you have installed `clang++`, `pylint` and `eslint` installed and have
correctly setup `$PATH`.

Edit line 81 in `frontend/src/components/UploadSource.vue` if the django server
is not running on http://localhost:8000 .

The `Upload` method/tab in frontend is buggy as errors are not highlighted properly
in the editor.

The `Text` method/tab should definitely work.

Checkout the [backend README](backend/README.md) for setting up backend
development server and [frontend README](frontend/README.md) for setting up
frontend development server.
