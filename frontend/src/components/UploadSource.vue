<template>
  <div class="container">
    <div class="large-12 medium-12 small-12 cell">
      <div class="inline-block">
        <input type="radio" v-model="by" value="Upload" checked>Upload<br>
      </div>
      <div class="inline-block">
        <input type="radio" v-model="by" value="Text">Text<br>
      </div>
      <div>
        <div>
          <label>Language
            <select v-model="language">
              <option value="cpp">C++</option>
              <option value="js">JavaScript</option>
              <option value="py">Python</option>
            </select>
          </label>
        </div>
        <div>
          <label v-show="by=='Text'">Text
            <textarea v-model="text" style="width: 500px; height: 500px;"></textarea>
          </label>
          <label v-show="by=='Upload'">File(Size limit is 100,000 bytes)
            <input type="file" id="file" ref="file" v-on:change="handleFileUpload()"/>
          </label>
        </div>
      </div>
      <div>
        <button :disabled="disableSubmit || file == '' && text == ''" v-on:click="submitFile()">Submit</button>
      </div>
      <div style="color: #faa">
        {{ error }}
      </div>
      <hr>
      <div v-show="output != ''">
        Results: <pre>{{ output }}</pre>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'UploadSource',
  data () {
    return {
      file: '',
      language: 'py',
      error: '',
      output: '',
      by: 'Upload',
      text: '',
      disableSubmit: false
    }
  },
  methods: {
    handleFileUpload () {
      this.file = this.$refs.file.files[0]
      if (this.file.size > 100000 || !this.file.type.match(/^text\//) || this.file.type === '') {
        this.file = ''
        this.error = 'Invalid file or it has an invalid type'
      } else {
        this.error = ''
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
      this.error = 'Processing'
      this.disableSubmit = true
      this.output = ''
      axios.post('http://localhost:8000/analyze/', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      }).then(response => {
        this.error = ''
        this.disableSubmit = false
        this.output = response.data.output + '\n' + response.data.error
        if (this.output.length === 1) {
          this.output = 'There was no output'
        }
      }).catch(() => {
        this.error = ''
        this.disableSubmit = false
        this.output = 'Server Error'
      })
    }
  }
}
</script>

<style>
  .inline-block {
    display: inline-block;
  }
</style>
