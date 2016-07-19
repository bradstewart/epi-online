const jetpack = require('fs-jetpack')
const path = require('path')
const _ = require('lodash')

const GROUP_SIZE = 4

const dataDir = jetpack.cwd(__dirname, '../', 'static', 'data')

dataDir
  .findAsync('posts', {
    matching: '*.json',
  })
  .then((paths) => {
    console.log(`Indexing ${paths.length} post files...`)

    return Promise.all(
      paths.map((p) => {
        return dataDir
          .readAsync(p, 'json')
          .then((post) => _.pick(post, ['slug', 'title']))
      })
    )
  })
  .then((posts) => {
    const groups = _.chunk(posts, GROUP_SIZE).map((group, index) => {
      return {
        id: index,
        title: `Group ${index}`,
        posts: group,
      }
    })

    return dataDir.writeAsync('posts.json', groups)
  })
  .then(() => {
    console.log('Indexing complete!')
  })
  .catch((err) => {
    console.error(err)
  })
