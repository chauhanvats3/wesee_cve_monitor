<template>
  <div class="tech-pill" @click="$emit('pill-clicked', tech)">
    <p :style="{ background: bgColors[2], color: bgColors[0] }">
      {{ tech.name }}
    </p>
    <p :style="{ background: bgColors[1], color: bgColors[0] }">
      {{ techVersion }}
    </p>
    <p :style="{ background: bgColors[0], color: bgColors[2] }">
      {{ tech.cves.length }}
    </p>

    <p
      v-if="hasNew"
      class="newIndicator"
      :style="{ background: bgColors[2], color: bgColors[0] }"
    ></p>
  </div>
</template>

<script>
export default {
  props: ['tech'],

  computed: {
    bgColors() {
      let hslValues = this.$generatePalette(this.tech.color)
      let bg = []
      for (let i = 0; i < hslValues.length; i++) {
        bg[
          i
        ] = `hsl(${hslValues[i][0]}deg, ${hslValues[i][1]}%,${hslValues[i][2]}%, ${hslValues[i][3]})`
      }
      //console.log(`${this.tech.name} : ${bg}`)
      return bg
    },
    techVersion() {
      let versions = this.tech.versions.arr
      if (versions.length == 0) return 'NA'
      if (versions.length > 1) return versions[0]
      return versions[0] == '' ? 'NA' : versions[0]
    },
    hasNew() {
      let cves = this.tech.cves
      for (let i = 0; i < cves.length; i++) {
        if (cves[i].isNew) return true
      }
      return false
    },
  },
}
</script>

<style lang="sass" scoped>
.tech-pill
    @include flexify-row
    margin: 0 20px
    cursor: pointer
    position: relative


    p
        margin: 20px 0px
        color: white
        padding: 10px 40px 10px 20px
        border-radius: 10px
    p:nth-child(1)
        margin-right: -20px
    p:nth-child(2)
        margin-right: -20px
    p:nth-child(3)
        padding-right: 20px

    .newIndicator
      position: absolute
      padding: 10px
      margin: 0
      right: -5px
      top: 15px
      font-size: 18px
</style>
