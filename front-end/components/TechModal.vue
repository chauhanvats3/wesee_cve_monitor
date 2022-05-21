<template>
  <div class="tech-modal" v-if="tech.name" @click.stop="">
    <div class="top-bar">
      <div>
        <p :style="{ background: bgColors[2], color: bgColors[0] }">
          {{ tech.name }}
        </p>
      </div>

      <div class="version">
        <p
          :style="{ background: bgColors[1], color: bgColors[0] }"
          ref="version"
        >
          {{ techVersion }}
        </p>
        <div class="newVer" ref="newVer">
          <input
            type="text"
            name="newVersion"
            id="newVersion"
            :style="{ background: bgColors[1], color: bgColors[0] }"
            v-model="newTechVer"
          />
          <p class="edit" @click.stop="okClicked">ok</p>
        </div>
        <p class="edit" @click.stop="editClicked">edit</p>
      </div>

      <div>
        <p :style="{ background: bgColors[0], color: bgColors[2] }">
          {{ tech.cves.length }} CVEs Found
        </p>
      </div>
    </div>
  </div>
</template>

<script>
import { mapActions } from 'vuex'

export default {
  props: ['tech'],
  data() {
    return {
      isEditing: false,
      newTechVer: '',
    }
  },
  methods: {
    ...mapActions({ updateTech: 'domains/updateTech' }),
    editClicked() {
      this.$refs.newVer.classList.add('show')
    },
    async okClicked() {
      console.log(this.newTechVer)
      if (
        this.newTechVer == '' ||
        !Number.isInteger(parseInt(this.newTechVer.replaceAll('.', '')))
      ) {
        this.newTechVer = ''
        this.$refs.newVer.classList.remove('show')
        return
      }

      this.tech.versions.arr[0] = this.newTechVer
      let status = await this.updateTech(this.tech)
      console.log(status)
      this.newTechVer = ''
      this.$refs.newVer.classList.remove('show')
    },
  },
  computed: {
    bgColors() {
      if (!this.tech.color) return []

      let color = this.tech.color
      let hslValues = this.$generatePalette(color)
      let bg = []
      for (let i = 0; i < hslValues.length; i++) {
        bg[
          i
        ] = `hsl(${hslValues[i][0]}deg, ${hslValues[i][1]}%,${hslValues[i][2]}%, ${hslValues[i][3]})`
      }
      return bg
    },
    techVersion() {
      let versions = this.tech.versions.arr
      if (versions.length == 0) return 'NA'
      if (versions.length > 1) return versions[0]
      return versions[0]
    },
  },
}
</script>

<style lang="sass" scoped>
.tech-modal
  width: 70%
  height: 70%
  @include flexify-col
  justify-content: flex-start
  border-radius: 15px
  background: white
  z-index: 2
  .top-bar
    width: 100%
    @include flexify-row
    justify-content: space-evenly
    div
      border-bottom-right-radius: 10px
      border-top-right-radius: 10px
      @include flexify-row
      flex-grow: 1
      position: relative
      overflow: hidden

      p
        color: white
        width: 100%
        @include flexify-row
        flex-grow: 1
        padding: 10px

        &.edit
          color: #f1f1f1
          cursor: pointer
          font-size: 16px
          position: absolute
          right: 0
          width: max-content

    div:nth-child(1)
          margin-right: -20px
          border-top-left-radius: 10px
          z-index: 2
    div:nth-child(2)
          margin-right: -20px
          z-index: 1
    div:nth-child(3)
          border-bottom-right-radius: 0
    .version
      .newVer
        position: absolute
        left: -100%
        width: 100%
        height: 100%
        transition: all 0.2s ease-in
        input
          height: 100%
          border-radius: 10px
          border: none
          outline: none
          padding:0 45px
          text-align: center
        &.show
          left: 0
</style>
