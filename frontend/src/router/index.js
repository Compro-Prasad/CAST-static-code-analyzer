import Vue from 'vue'
import Router from 'vue-router'
import UploadSource from '@/components/UploadSource'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'UploadSource',
      component: UploadSource
    }
  ]
})
