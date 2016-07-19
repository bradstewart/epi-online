import AceEditor from './AceEditor'
import LoadBar from './LoadBar'
import LogOutput from './LogOutput'
import Modal from './Modal'
import Panel from './Panel'

function install (Vue) {
  Vue.component('ace-editor', AceEditor)
  Vue.component('load-bar', LoadBar)
  Vue.component('log-output', LogOutput)
  Vue.component('modal', Modal)
  Vue.component('panel', Panel)
}

export {
  AceEditor,
  LoadBar,
  LogOutput,
  Modal,
  Panel,
}

export default {
  install,
}
