<template>
  <div class="row flex-middle">
    <at-card class="col-20 col-offset-2">
      <div class="row flex-center">
        <at-radio-group v-model="by">
          <at-radio-button label="Upload" checked>Upload</at-radio-button>
          <at-radio-button label="Text">Text</at-radio-button>
        </at-radio-group>
      </div>
      <div style="margin: 10px">
        <div class="row flex-center">
          <label class="col-6">Language</label>
          <at-select :disabled="disableSubmit"
            class="col-6" size="large" v-model="language">
            <at-option value="cpp">C++</at-option>
            <at-option value="js">JavaScript</at-option>
            <at-option value="py">Python</at-option>
          </at-select>
        </div>
        <div>
          <editor-box v-show="by=='Text'" :language="language" :code.sync="text" :errors.sync="fileErrors" />
          <input :disabled="disableSubmit"
            v-show="by=='Upload'" type="file" id="file" ref="file" v-on:change="handleFileUpload()" />
        </div>
      </div>
      <div>
        <at-button :disabled="disableSubmit || file == '' && text == ''" v-on:click="submitFile()">Submit</at-button>
      </div>
      <hr>
      <div v-show="output != ''">
        Results: <pre>{{ output }}</pre>
      </div>
    </at-card>
  </div>
</template>

<script>
import axios from 'axios'
import EditorBox from '@/components/editor-box'

export default {
  name: 'UploadSource',
  data () {
    return {
      file: '',
      fileName: '',
      fileErrors: [],
      language: 'py',
      output: '',
      by: 'Text',
      text: '',
      disableSubmit: false
    }
  },
  methods: {
    handleFileUpload () {
      this.file = this.$refs.file.files[0]
      if (this.file.size > 100000 || !this.file.type.match(/^text\//) || this.file.type === '') {
        this.file = ''
        this.$Notify.error({
          'message': 'Size limit is 100,000 bytes or invalid file type',
          'duration': 0
        })
      } else {
      }
    },
    submitFile () {
      let formData = new FormData()
      if (this.by === 'Upload' && this.file !== '') {
        formData.set('file', this.file)
      } else if (this.by === 'Text' && this.text !== '') {
        formData.set('text', this.text)
      } else {
        return
      }
      formData.set('by', this.by.toLowerCase())
      formData.set('language', this.language)
      this.disableSubmit = true
      this.$Notify.info({ message: 'Processing', duration: 20000 })
      this.output = ''
      axios.post('http://localhost:8000/analyze/', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      }).then(response => {
        if (this.by === 'Upload') {
          this.text = response.data.text
        }
        this.output = response.data.output
        this.fileErrors = response.data.errors
        this.fileName = response.data.file
        this.by = 'Text'
        if (this.output.length === 1 && this.fileErrors.length === 0) {
          this.$Notify.info({ message: 'No output recieved', duration: 20000 })
        } else {
          this.$Notify.info({ message: 'Got some output', duration: 20000 })
        }
        this.disableSubmit = false
      }).catch(() => {
        this.$Notify.error({ message: 'Server error', duration: 20 })
        this.disableSubmit = false
      })
    }
  },
  watch: {
    language: function () {
      if (this.disableSubmit && this.fileErrors.length !== 0) {
        this.fileErrors.splice(0, this.fileErrors.length)
      }
    }
  },
  components: {
    EditorBox
  }
}
</script>

<style>
.inline-block {
  display: inline-block;
}
</style>
