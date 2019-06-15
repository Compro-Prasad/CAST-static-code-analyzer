// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import VueCodemirror from 'vue-codemirror'
import AtComponents from 'at-ui'
import 'at-ui-style'

// import 'at-ui-style/src/index.scss'      // Or import the unbuilt version of SCSS

// require styles
import 'codemirror/lib/codemirror.css'

// require more codemirror resource...

// you can set default global options and events when use
Vue.use(VueCodemirror, {
  options: {theme: 'base16-dark'},
  events: ['scroll']
})

Vue.use(AtComponents)
Vue.config.productionTip = false

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  components: { App },
  template: '<App/>'
})
