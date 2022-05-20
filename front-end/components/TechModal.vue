<template>
  <div class="tech-modal" @click.stop="modalClicked" v-if="tech.name">
    <div class="top-bar">
      <p :style="{ background: bgColors[2], color: bgColors[0] }">
        {{ tech.name }}
      </p>
      <p :style="{ background: bgColors[1], color: bgColors[0] }">
        {{ techVersion }}
        <span class="edit">edit</span>
      </p>
      <p :style="{ background: bgColors[0], color: bgColors[2] }">
        {{ tech.cves.length }} CVEs Found
      </p>
    </div>
  </div>
</template>

<script>
export default {
  props: ['tech'],
  methods: {
    modalClicked() {
      console.log(this.tech.color)
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
      if (versions.length > 1) return 'multiple'
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
    p
      color: white
      flex-grow: 1
      padding: 10px 30px
      border-bottom-right-radius: 10px
      border-top-right-radius: 10px
      @include flexify-row
      position: relative
      .edit
        color: #f1f1f1
        cursor: pointer
        margin: 0 20px 0 10px
        font-size: 16px
        position: absolute
        right: 0

    p:nth-child(1)
        margin-right: -20px
        border-top-left-radius: 10px
        z-index: 2
    p:nth-child(2)
        margin-right: -20px
        z-index: 1
    p:nth-child(3)
        padding-right: 20px
        border-bottom-right-radius: 0
</style>
