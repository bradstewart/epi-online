const INSERT = '//INSERT_ME'

export const Java = {
  text: 'Java',
  value: 'java',
  aceEditorId: 'java',
  compileBoxId: 8,
  assemble: ({ harness, package: _package, imports, skeleton }) => {
    return `
      ${_package}
      ${imports}
      ${harness.replace(INSERT, skeleton)}
    `
  }
}

export const Cpp = {
  text: 'C/C++',
  value: 'cpp',
  aceEditorId: 'c_cpp',
  compileBoxId: 7,
  assemble: ({ harness, skeleton }) => {
    return harness.replace(INSERT, skeleton)
  }
}
