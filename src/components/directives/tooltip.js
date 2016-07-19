
export default {
  params: [
    'delay',
    'viewport',
    'container',
  ],

  bind () {
    this._content = ''

    $(this.el).tooltip({
      title: () => this._content,
      placement: this._getPosition(),
      viewport: this.params.viewport || false,
      delay: this.params.delay || 0,
      container: this.params.container || 'body',
    })
  },

  update (value) {
    this._content = value
  },

  unbind () {
    $(this.el).tooltip('destroy')
  },

  _getPosition () {
    return Object.keys(this.modifiers).find((m) => {
      return m === 'top'
              || m === 'bottom'
              || m === 'left'
              || m === 'right'
    })
  },
}
