<template>
  <div class="cve" :style="{ background: severityColorPalette[2] }">
    <div class="top">
      <div class="ratings">
        <div
          class="score"
          :style="{
            background: severityColorPalette[1],
            color: severityColorPalette[0],
          }"
        >
          {{ source.score }}
        </div>
        <div
          class="severity"
          :style="{
            color: severityColorPalette[0],
          }"
        >
          {{ source.severity }}
        </div>
      </div>
      <div class="references" @click.stop="openReferences">
        <p>Open {{ source.references.arr.length }} References</p>
      </div>
    </div>
    <div class="description">
      <p>
        {{ source.description }}
      </p>
    </div>
  </div>
</template>

<script>
export default {
  props: ['source'],
  methods: {
    openReferences() {
      console.log(this.cve)
      for (let i = 0; i < this.source.references.arr.length; i++)
        window.open(this.source.references.arr[i], '_blank')
    },
  },
  computed: {
    severityColorPalette() {
      if (this.source.severity.toLowerCase() == 'low') {
        return ['#00A7C2', '#00A7C245', '#00A7C225']
      }
      if (this.source.severity.toLowerCase() == 'medium') {
        return ['#ffc302', '#ffc30245', '#ffc30225']
      }
      if (this.source.severity.toLowerCase() == 'high') {
        return ['#ff5b00', '#ff5b0045', '#ff5b0025']
      }
      if (this.source.severity.toLowerCase() == 'critical') {
        return ['#c80000', '#c8000045', '#c8000025']
      }
    },
  },
}
</script>

<style lang="sass" scoped>
.cve
    margin: 80px auto 150px
    border-radius: 10px
    width: 90%
    padding-bottom: 1px
    .top
        @include flexify-row
        justify-content: space-between
        .ratings
            @include flexify-row
            color: white
            width: max-content
            margin-left: -25px
            margin-top: -40px


            .score
                font-size: 2rem
                color: white
                padding: 10px
                border-radius: 5px
                -webkit-backdrop-filter: blur(5px)
                backdrop-filter: blur(5px)

            .severity
                font-size: 0.75rem
                border-radius: 5px
                padding: 10px 20px
                width: 100%
                display: flex
                justify-content: center
                letter-spacing: 5px
                align-self: flex-start


        .references
            margin-top: -35px
            cursor: pointer
            font-size: 0.75rem
            align-self: flex-start
            height: 100%
            margin-right: 20px
            color: $main-color
    .description
        margin: 30px auto
        padding: 10px 20px
        font-size: 0.9rem
        word-spacing: 0.2rem
        line-height: 1.5rem
        letter-spacing: 0.01rem
        max-width: 55ch
        margin-bottom: 70px
</style>
