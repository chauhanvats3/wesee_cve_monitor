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
            v-if="!storeTech.updating_cve"
          />
          <p class="edit" @click.stop="okClicked">ok</p>
        </div>
        <p
          class="edit"
          @click.stop="editClicked"
          v-if="!storeTech.updating_cve"
        >
          edit
        </p>
      </div>

      <div>
        <p :style="{ background: bgColors[0], color: bgColors[2] }">
          {{ tech.cves.length }} CVEs Found
        </p>
      </div>
    </div>
    <div class="cves">
      <CVE v-for="(cve, index) in tech.cves" :key="index" :source="cve" />
    </div>
    <div class="updating" v-if="storeTech.updating_cve">
      <p>Updating CVEs...</p>
    </div>
  </div>
</template>

<script>
import { mapActions, mapGetters } from 'vuex'
import CVE from './CVE'
import VirtualList from 'vue-virtual-scroll-list'
export default {
  props: ['tech'],
  components: { 'virtual-list': VirtualList },
  data() {
    return {
      cveComponent: CVE,
      isEditing: false,
      newTechVer: '',
      noOfItems: 20,
      sizeOfItem: 300,
    }
  },
  methods: {
    ...mapActions({ updateTech: 'domains/updateTechBackend' }),
    editClicked() {
      this.$refs.newVer.classList.add('show')
      this.newTechVer = this.techVersion
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
      if (this.newTechVer == this.techVersion) {
        console.log('same version')
        this.$refs.newVer.classList.remove('show')
        return
      }
      let newVer = this.newTechVer
      this.tech.versions.arr[0] = this.newTechVer
      this.newTechVer = ''
      this.$refs.newVer.classList.remove('show')
      let status = await this.updateTech({
        id: this.tech.id,
        newVer: newVer,
      })
      console.log(status)
    },
  },
  computed: {
    ...mapGetters({ getTechStore: 'domains/getTechFromStore' }),
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
      let versions = this.storeTech.versions.arr
      if (versions.length == 0) return 'NA'
      if (versions.length > 1) return versions[0]
      return versions[0] == '' ? 'NA' : versions[0]
    },
    storeTech() {
      return this.getTechStore(this.tech.id)
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
  overflow-y: scroll
  position: relative
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
        padding: 15px 10px

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
          z-index: 3
    div:nth-child(2)
          margin-right: -20px
          z-index: 2
    div:nth-child(3)
          z-index: 1
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
  .cves
    width: 100%
    height: 100%
    overflow-y: scroll
    position: relative
  .updating
    @include flexify-col
    position: absolute
    width: 100%
    height: 100%
    color: white
    top: 0
    left: 0
    background: rgba(72, 72, 72, 0.44)
    backdrop-filter: blur(9.4px)
    -webkit-backdrop-filter: blur(9.4px)
</style>
