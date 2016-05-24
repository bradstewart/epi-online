
export const tooltip = {
  params: ['delay'],

  bind () {
    /* no op */
  },

  update (value) {
    this.el.dataset['tooltip'] = value
    this.el.dataset['position'] = this._getPosition() || 'bottom'

    $(this.el).tooltip({
      delay: this.params.delay || 50,
    })
  },

  unbind () {
    $(this.el).tooltip('remove')
  },

  _getPosition () {
    return Object.keys(this.modifiers).find((m) => {
      return m === 'top'
              || m === 'bottom'
              || m === 'left'
              || m === 'right'
    })
  }
}
