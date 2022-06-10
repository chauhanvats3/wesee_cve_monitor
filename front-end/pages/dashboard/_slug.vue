<template>
  <div class="dashboard-slug">
    <Nav />
    <p v-if="$fetchState.pending">Fetching Domains...</p>
    <div v-else>
      <div class="top-row">
        <h1 ref="h1">
          {{ thisDomain.name }}
        </h1>
        <div class="cron">
          <p>update CVEs every</p>
          <select
            name="cron-interval"
            id="cron-interval"
            v-model="cronInterval"
          >
            <option value="2">two</option>
            <option value="4">four</option>
            <option value="6">six</option>
            <option value="8">eight</option>
            <option value="10">ten</option>
            <option value="12">twelve</option>
          </select>
          <p>hours</p>
        </div>
      </div>

      <div class="techs">
        <TechPill
          v-for="(tech, index) in thisDomain.techs"
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
            v-model="enumerate"
          />
          <p
            @click="checkBoxClick"
            style="cursor: pointer; letter-spacing: 2px"
          >
            Enumerate Subdomains?
          </p>
        </div>
        <div class="addSubDomain">
          <input
            type="text"
            name="subdomain"
            id="subDomainTxt"
            ref="newSubdomain"
            placeholder="https://"
            v-model="newSubdomainName"
          />
          <div class="btn add-subdomain" @click="addSubdomain">
            <p>Add Subdomain</p>
          </div>
        </div>
      </div>
      <Subdomains
        v-if="enumerate"
        :domain="slug"
        v-on:sub-pill-clicked="openSubTechDetails"
      />
      <ExcludedSubdomains :domain="slug" v-if="enumerate && excludedExist" />
    </div>
  </div>
</template>

<script>
import { mapGetters, mapActions, mapMutations } from 'vuex'

export default {
  middleware: 'auth',

  data() {
    return {
      techToOpen: {},
      enumSubdomains: false,
      excludedSubdomainsExist: false,
      newSubdomainName: '',
      isEditing: false,
    }
  },
  async asyncData(context) {
    const slug = context.params.slug
    return { slug }
  },

  computed: {
    ...mapGetters({
      domains: 'domains/getAllDomains',
      domainInfo: 'domains/getDomainInfo',
      getExcluded: 'domains/getExcludedSubdomains',
    }),
    thisDomain() {
      let info = this.domainInfo(this.slug)
      if (info == undefined) {
        return {
          name: '',
          techs: [],
        }
      }
      return info
    },
    excludedExist() {
      let excludedSubdomains = this.getExcluded(this.slug)
      return excludedSubdomains.length == 0 ? false : true
    },
    enumerate: {
      get() {
        return this.domainInfo(this.slug, 'enumerate')
      },
      set() {
        //this.enumToggle(this.slug)
        this.toggleEnumerateBackend(this.domainInfo(this.slug))
      },
    },
    cronInterval: {
      get() {
        return this.thisDomain.cron_interval
      },
      set(newValue) {
        this.changeCron({ id: this.thisDomain.id, cronInterval: newValue })
      },
    },
  },
  methods: {
    ...mapActions({
      subdomainToBackend: 'domains/addSubdomainToBackend',
      getDomainsFromBackend: 'domains/getDomainsFromBackend',
      toggleEnumerateBackend: 'domains/toggleEnumeration',
      toggleCVESeenBackend: 'domains/toggleCVESeen',
      changeCron: 'domains/changeCronInterval',
    }),
    ...mapMutations({
      enumToggle: 'domains/enumToggle',
    }),
    openTechDetails(tech) {
      this.techToOpen = tech
      this.$refs.techModalWrapper.classList.add('show')
    },
    openSubTechDetails(info) {
      this.techToOpen = info.tech
      this.$refs.techModalWrapper.classList.add('show')
    },
    closeModal() {
      this.toggleCVESeenBackend(this.techToOpen.id)
      this.$refs.techModalWrapper.classList.remove('show')
    },
    checkBoxClick() {
      this.toggleEnumerateBackend(this.domainInfo(this.slug))
    },
    addSubdomain() {
      let name = this.newSubdomainName.split('://').pop()
      if (name.search(this.slug) == -1) name = name + '.' + this.slug
      let domainId = this.thisDomain.id
      this.subdomainToBackend({
        domainName: this.slug,
        subdomainName: name,
        include: true,
        domainId,
      })
      this.newSubdomainName = ''
    },
  },
  async fetch() {
    let storedDomains = this.$store.getters['domains/getAllDomains']
    if (storedDomains.length == 0) await this.getDomainsFromBackend()
  },
  fetchOnServer: false,
}
</script>

<style lang="sass" scoped>
.dashboard-slug
  position: relative
  padding: 0 3.5%
  padding-top: 120px

  .top-row
    @include flexify-row
    justify-content: space-between

    .cron
      @include flexify-row
      font-size: 0.75rem
      p
        margin: 5px 5px
      select
        background: white
        color: $main-color
        outline: none
        text-align: center
        border: none
        resize: none
        outline: none
        cursor: pointer
        -webkit-appearance: none
        -moz-appearance: none
        appearance: none
        text-indent: 1px
        text-overflow: ''

  .techs
    @include flexify-row
    flex-wrap: wrap !important
    margin: 50px 0
    padding: 0 2%

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
    z-index: 5

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
    .addSubDomain
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
