import 'bootstrap'
import 'keen-ui/dist/keen-ui.css'

import Vue from 'vue'
import VueRouter from 'vue-router'
import VueResource from 'vue-resource'
import KeenUI from 'keen-ui'
import AppDirectives from './components/directives'
import AppComponents from './components/common'

Vue.use(VueRouter)
Vue.use(VueResource)
Vue.use(KeenUI)
Vue.use(AppDirectives)
Vue.use(AppComponents)

import App from './App'
import ProblemsIndex from './components/ProblemsIndex'
import ProblemsView from './components/ProblemsView'
import ProblemsTestView from './components/ProblemsTestView'

const router = new VueRouter({
  linkActiveClass: 'active',
})

router.map({
  '/': {
    name: 'problems',
    component: ProblemsIndex,
  },
  '/:group/:id': {
    name: 'problem',
    component: ProblemsView,
  },
  '/problems/test': {
    name: 'problems.test',
    component: ProblemsTestView,
  }
})

router.start(App, '#app')
