<template>
  <at-card>
    <div class="md-subhead">
      <span>mode: {{ cmOption.mode }}</span>
      <span>&nbsp;&nbsp;&nbsp;</span>
      <span>theme: {{ cmOption.theme }}</span>
    </div>
    <div class="vue">
      <div class="codemirror">
        <codemirror v-model="text"
          :options="cmOption"
          @ready="onCmReady">
        </codemirror>
      </div>
    </div>
  </at-card>
</template>

<script>
// language
import 'codemirror/mode/clike/clike.js'
import 'codemirror/mode/python/python.js'
import 'codemirror/mode/javascript/javascript.js'
// theme css
import 'codemirror/theme/base16-light.css'
// active-line.js
import 'codemirror/addon/selection/active-line.js'
// styleSelectedText
import 'codemirror/addon/selection/mark-selection.js'
// highlightSelectionMatches
import 'codemirror/addon/scroll/annotatescrollbar.js'
import 'codemirror/addon/search/matchesonscrollbar.js'
import 'codemirror/addon/search/match-highlighter.js'
// keyMap
import 'codemirror/addon/edit/matchbrackets.js'
import 'codemirror/addon/comment/comment.js'
import 'codemirror/addon/dialog/dialog.js'
import 'codemirror/addon/dialog/dialog.css'
import 'codemirror/addon/search/search.js'
import 'codemirror/keymap/sublime.js'
// foldGutter
import 'codemirror/addon/fold/foldgutter.css'
import 'codemirror/addon/fold/brace-fold.js'
import 'codemirror/addon/fold/comment-fold.js'
import 'codemirror/addon/fold/foldcode.js'
import 'codemirror/addon/fold/foldgutter.js'
import 'codemirror/addon/fold/indent-fold.js'
import 'codemirror/addon/fold/markdown-fold.js'
import 'codemirror/addon/fold/xml-fold.js'
export default {
  props: {
    language: String,
    code: String,
    errors: {
      required: false,
      default () { return [] },
      type: Array
    },
    warnings: {
      required: false,
      default () { return [] },
      type: Array
    }
  },
  data () {
    const modes = {
      'cpp': 'text/x-c++src',
      'js': 'text/javascript',
      'py': 'text/x-python'
    }
    return {
      modes,
      cm: {},
      cm_doc: {},
      line_errors: [],
      text: this.code,
      cmOption: {
        tabSize: 4,
        foldGutter: true,
        styleActiveLine: true,
        lineNumbers: true,
        line: true,
        keyMap: 'sublime',
        mode: modes[this.language],
        theme: 'base16-light'
      }
    }
  },
  watch: {
    language: function (newlang, oldlang) {
      this.cmOption.mode = this.modes[newlang]
    },
    errors: function (newerrors, olderrors) {
      for (let error of this.line_errors) {
        this.cm_doc.removeLineClass(error['handle'], 'background', 'error-class')
        error['widget'].clear()
      }
      this.line_errors.splice(0, this.line_errors.length)
      for (let error of newerrors) {
        if (this.cm_doc.lineInfo(error['line'])) {
          this.line_errors.push({
            'handle': this.cm_doc.addLineClass(error['line'], 'background', 'error-class'),
            'widget': this.cm_doc.addLineWidget(error['line'], this.newError(error['text']))
          })
        }
      }
    },
    text: function (newcode, oldcode) {
      this.$emit('update:code', newcode)
    }
  },
  warnings: function (newwarnings, oldwarnings) {
    for (let warning of oldwarnings) {
      this.cm_doc.removeLineClass(warning['line'], 'background', 'warning-class')
    }
    for (let lineWidgetWarn of this.line_widget_warns) {
      lineWidgetWarn.clear()
    }
    this.line_widget_warns.length = 0
    for (let warning of newwarnings) {
      if (this.cm_doc.lineInfo(warning['line'])) {
        this.cm_doc.addLineClass(warning['line'], 'background', 'warning-class')
        this.line_widget_warns.push(this.cm_doc.addLineWidget(
          warning['line'],
          this.newWarning(warning['text'])
        ))
      }
    }
  },
  methods: {
    newError (text) {
      return this.createElementFromHTML(
        '<div class="error-text">' +
        text +
        '</div>'
      )
    },
    newWarning (text) {
      return this.createElementFromHTML(
        '<div class="warning-text">' +
        text +
        '</div>'
      )
    },
    createElementFromHTML (htmlString) {
      var div = document.createElement('div')
      div.innerHTML = htmlString.trim()
      return div.firstChild
    },
    onCmReady (codemirror) {
      this.cm = codemirror
      this.cm_doc = codemirror.getDoc()
    }
  }
}
</script>

<style>
.error-class {
  background-color: #f00 !important;
  opacity: 0.2;
}
.warning-class {
  background-color: #ff0 !important;
  opacity: 0.2;
}
.error-text {
  background-color: #fff !important;
  color: #f00 !important;
}
.warning-text {
  background-color: #fff !important;
  color: #ff0 !important;
}
</style>
