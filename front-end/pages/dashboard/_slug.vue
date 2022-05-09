<template>
  <div class="dashboard-slug">
    <Nav />
    <ul>
      <li v-for="domain in getDomainInfo(slug)" :key="domain.name">
        <h1>
          {{ domain.name }}
        </h1>

        <div class="techs">
          <TechPill
            v-for="(tech, index) in domain.techs"
            :key="index"
            :tech="tech"
            v-on:pill-clicked="openTechDetails"
          />
        </div>
        <div
          class="modal-wrapper"
          ref="techModalWrapper"
          @click.stop="closeModal"
        >
          <TechModal :tech="techToOpen" />
        </div>

        <div class="options">
          <div class="enum">
            <input
              type="checkbox"
              name="enumerate"
              id="enumChkbx"
              ref="chkbxEnum"
            />
            <p
              @click="checkBoxClick"
              style="cursor: pointer; letter-spacing: 2px"
            >
              Enumerate Subdomains?
            </p>
          </div>
          <div class="addDomain">
            <input
              type="text"
              name="subdomain"
              id="subDomainTxt"
              ref="newSubdomain"
              placeholder="https://"
            />
            <div class="btn add-subdomain" @click="addNewSubdomain">
              <p>Add Subdomain</p>
            </div>
          </div>
        </div>

        <Subdomains :domain="slug" v-on:sub-pill-clicked="openSubTechDetails" />
      </li>
    </ul>
    <ExcludedSubdomains :domain="slug" />
  </div>
</template>

<script>
import { mapGetters, mapMutations } from 'vuex'

export default {
  async asyncData({ params }) {
    const slug = params.slug
    return { slug }
  },
  data() {
    return {
      techToOpen: {
        name: 'VueJs',
        ver: '2.5.4',
        cves: ['This is a dummy CVE 1', 'Dummy CVE 2', 'CVE 3'],
        color: '#42b883',
      },
    }
  },
  mounted() {
    console.log(this.slug)
    let defaultTech = this.getDomainInfo(this.slug)[0].techs[0]
    this.techToOpen = defaultTech
  },
  computed: {
    ...mapGetters('dashboard', ['getDomainInfo', 'getSubdomains']),
  },
  methods: {
    ...mapMutations({
      addSubdomain: 'dashboard/addSubdomain',
    }),
    openTechDetails(tech) {
      this.techToOpen = tech
      this.$refs.techModalWrapper[0].classList.add('show')
    },
    openSubTechDetails(info) {
      this.techToOpen = info.tech
      this.$refs.techModalWrapper[0].classList.add('show')
    },
    closeModal() {
      this.$refs.techModalWrapper[0].classList.remove('show')
    },
    checkBoxClick() {
      this.$refs.chkbxEnum[0].checked = !this.$refs.chkbxEnum[0].checked
    },
    addNewSubdomain() {
      let info = {
        domain: this.slug,
        subdomain: this.$refs.newSubdomain[0].value,
      }
      this.addSubdomain(info)
      this.$refs.newSubdomain[0].value = ''
    },
  },
}
</script>

<style lang="sass" scoped>
.dashboard-slug
  position: relative
  padding-top: 120px
  ul
    width: 100%
    padding: 2% 5%
    padding-bottom: 0

  .techs
    @include flexify-row
    flex-wrap: wrap
    margin: 50px 0

  .modal-wrapper
    width: 100vw
    height: 100vh
    opacity: 0
    background: rgba(73, 73, 73, 0.65)
    backdrop-filter: blur(10px)
    @include flexify-row
    position: fixed
    top: 0
    left: 100%
    transform: scale(0)
    transition: all 0.4s ease-in-out

    &.show
      opacity: 1
      left: 0
      transform: scale(1)

  .options
    @include flexify-col
    width: 100%
    margin: 60px 0px
    justify-content: flex-start
    align-items: flex-start
    .enum
      margin: 50px 20px
      @include flexify-row
      input
        margin: 5px 30px 5px 10px
        width: 30px
        height: 30px
      p
        font-size: 1rem
    .addDomain
      padding: 0 20px
      @include flexify-row
      width: 100%
      justify-content: flex-start
      input
        flex-grow: 1
        border: none
        padding: 15px
        padding-right: 40px
        border-radius: 10px
        margin: 0 10px
        background: #F0F0F0
        color: $black
      div
        padding: 10px
        background: $main-color
        border-radius: 10px
        padding: 18px 25px
        margin-left: -40px
        cursor: pointer
        p
          color: white
</style>
