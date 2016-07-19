
export default {
  params: [
    'delay',
    'viewport',
    'container',
  ],

  bind () {
    this._content = ''

    $(this.el).popover({
      content: () => this._content,
      placement: this._getPosition(),
      viewport: this.params.viewport,
      delay: this.params.delay,
      container: this.params.container,
    })
  },

  update (value) {
    this._content = value
  },

  unbind () {
    $(this.el).popover('destroy')
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
