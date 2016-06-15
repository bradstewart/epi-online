
export const tooltip = {
  params: ['delay'],

  bind () {
    /* no op */
  },

  update (value) {
    if (!value) {
      return
    }
    
    this.el.dataset['title'] = value
    console.log(value)
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
