import 'bootstrap'

import Vue from 'vue'
import VueRouter from 'vue-router'
import VueResource from 'vue-resource'

Vue.use(VueRouter)
Vue.use(VueResource)

import * as commonComponents from './components/common'
// Install common components globally so individual components
// do not each have to import and install them.
Object.keys(commonComponents).forEach((name) => {
  Vue.component(name, commonComponents[name])
})

import * as commonDirectives from './components/common/directives'
// Install common components globally so individual components
// do not each have to import and install them.
Object.keys(commonDirectives).forEach((name) => {
  console.log(name)
  Vue.directive(name, commonDirectives[name])
})

import App from './App'
import ProblemsIndex from './components/ProblemsIndex'
import ProblemsView from './components/ProblemsView'

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
  }
})

router.start(App, '#app')
