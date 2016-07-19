import 'bootstrap'

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
import ProblemsShow from './components/ProblemsShow'
import ProblemsShowTest from './components/ProblemsShowTest'

const router = new VueRouter({
  linkActiveClass: 'active',
})

router.map({
  '/problems': {
    name: 'problems.index',
    component: ProblemsIndex,
  },
  '/problems/:group/problem/:id': {
    name: 'problems.show',
    component: ProblemsShow,
  },
  '/problems/test': {
    name: 'problems.test',
    component: ProblemsShowTest,
  }
})

router.redirect({
  '/': '/problems',
})

router.start(App, '#app')
