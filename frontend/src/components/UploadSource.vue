<template>
  <div class="container">
    <div class="large-12 medium-12 small-12 cell">
      <input type="radio" v-model="by" value="Upload" checked>Upload<br>
      <input type="radio" v-model="by" value="Text">Text<br>
      <label>Language
        <select v-model="language">
          <option value="cpp">C++</option>
          <option value="js">JavaScript</option>
          <option value="py">Python</option>
        </select>
      </label>
      <label v-show="by=='Text'">Text
        <textarea v-model="text" style="width: 100px; height: 100px;"></textarea>
      </label>
      <label v-show="by=='Upload'">File
        <input type="file" id="file" ref="file" v-on:change="handleFileUpload()"/>
      </label>
      <button :disabled="error != ''" v-on:click="submitFile()">Submit</button>
      {{ error }}
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
      text: ''
    }
  },
  methods: {
    handleFileUpload () {
      this.file = this.$refs.file.files[0]
      if (this.file.size > 100000 || !this.file.type.match(/^text\//) || this.file.type === '') {
        this.file = ''
        this.error = 'File size is more than 100,000 bytes or it has an invalid type'
      } else {
        this.error = ''
      }
    },
    submitFile () {
      let formData = new FormData()
      if (this.by === 'Upload') {
        formData.set('file', this.file)
      } else if (this.by === 'Text') {
        formData.set('text', this.text)
      } else {
        this.error = 'Invalid source upload'
        return
      }
      formData.set('by', this.by.toLowerCase())
      formData.set('language', this.language)
      this.error = 'Processing'
      axios.post('http://localhost:8000/analyze/', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      }).then(response => {
        this.error = ''
        this.output = response.data.output + '\n' + response.data.error
        if (this.output.length == 1)
          this.output = "There was no output"
      }).catch(function () {
        this.output = "Server Error"
      })
    }
  }
}
</script>
