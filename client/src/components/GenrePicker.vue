<script setup lang="ts">
// @ai-generated true 2026-06-18
// 文件名: components/GenrePicker.vue
// 作用: 类型偏好选择弹窗 - 预设标签 + 自定义输入
import { ref, computed, watch } from 'vue'

const props = defineProps<{
  visible: boolean
  title: string
  selected: string[]
  excluded?: string[] // 互斥列表（喜欢/不喜欢不可重复）
  variant?: 'like' | 'dislike'
}>()

const emit = defineEmits<{
  (e: 'update:visible', v: boolean): void
  (e: 'confirm', list: string[]): void
}>()

// @ai-generated true 2026-06-18
// 预设的常见影视类型池
const PRESET_GENRES = [
  '悬疑推理', '韩剧', '日剧', '美剧', '英剧', '国产剧',
  '动画', '科幻', '喜剧', '爱情', '恐怖', '奇幻',
  '纪录片', '综艺', '动作', '文艺', '历史', '战争',
  '治愈', '美食', '青春', '家庭', '犯罪', '狗血',
]

// @ai-generated true 2026-06-18
// 本地工作副本，确认前不写回父组件
const draft = ref<string[]>([])
const customInput = ref('')

// @ai-generated true 2026-06-18
// 弹窗每次打开时同步父组件值
watch(
  () => props.visible,
  (v) => {
    if (v) {
      draft.value = [...props.selected]
      customInput.value = ''
    }
  }
)

// @ai-generated true 2026-06-18
// 已被互斥列表占用的类型不可选
const excludedSet = computed(() => new Set(props.excluded || []))

// @ai-generated true 2026-06-18
function toggle(g: string) {
  if (excludedSet.value.has(g)) {
    uni.showToast({
      title: `「${g}」已在另一组中`,
      icon: 'none',
    })
    return
  }
  const idx = draft.value.indexOf(g)
  if (idx >= 0) {
    draft.value.splice(idx, 1)
  } else {
    draft.value.push(g)
  }
}

// @ai-generated true 2026-06-18
function addCustom() {
  const v = customInput.value.trim()
  if (!v) return
  if (excludedSet.value.has(v)) {
    uni.showToast({ title: `「${v}」已在另一组中`, icon: 'none' })
    return
  }
  if (!draft.value.includes(v)) {
    draft.value.push(v)
  }
  customInput.value = ''
}

// @ai-generated true 2026-06-18
function onClose() {
  emit('update:visible', false)
}

// @ai-generated true 2026-06-18
function onConfirm() {
  emit('confirm', [...draft.value])
  emit('update:visible', false)
}

// @ai-generated true 2026-06-18
function isSelected(g: string) {
  return draft.value.includes(g)
}
</script>

<template>
  <view v-if="visible" class="gp">
    <!-- 遮罩 -->
    <view class="gp__mask" @tap="onClose"></view>

    <!-- 底部弹窗 -->
    <view class="gp__sheet">
      <view class="gp__head">
        <text class="gp__title">{{ title }}</text>
        <text class="gp__close" @tap="onClose">✕</text>
      </view>

      <!-- 已选预览 -->
      <view class="gp__selected">
        <text v-if="draft.length === 0" class="gp__selected-empty">
          暂未选择，点击下方标签添加
        </text>
        <view
          v-for="g in draft"
          :key="g"
          class="gp__chip gp__chip--sel"
          :class="`gp__chip--sel-${variant || 'like'}`"
          @tap="toggle(g)"
        >
          {{ g }} ✕
        </view>
      </view>

      <view class="divider"></view>

      <!-- 预设池 -->
      <text class="gp__label">常用类型</text>
      <view class="gp__grid">
        <view
          v-for="g in PRESET_GENRES"
          :key="g"
          class="gp__chip"
          :class="{
            'gp__chip--active': isSelected(g),
            'gp__chip--disabled': excludedSet.has(g),
          }"
          @tap="toggle(g)"
        >
          {{ isSelected(g) ? '✓ ' : '' }}{{ g }}
        </view>
      </view>

      <!-- 自定义输入 -->
      <text class="gp__label">自定义添加</text>
      <view class="gp__input-row">
        <input
          v-model="customInput"
          class="gp__input"
          placeholder="输入类型，如「悬疑推理」"
          placeholder-style="color:#5c586e"
          confirm-type="done"
          @confirm="addCustom"
        />
        <button class="rx-btn rx-btn--primary gp__add" @tap="addCustom">
          添加
        </button>
      </view>

      <!-- 操作 -->
      <view class="gp__actions">
        <button class="rx-btn rx-btn--ghost gp__act" @tap="onClose">
          取消
        </button>
        <button class="rx-btn rx-btn--primary gp__act" @tap="onConfirm">
          保存
        </button>
      </view>
    </view>
  </view>
</template>

<style scoped lang="scss">
/* @ai-generated true 2026-06-18 */
@import "@/styles/variables.scss";

.gp {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: 999;
  display: flex;
  flex-direction: column;
  justify-content: flex-end;

  &__mask {
    position: absolute;
    inset: 0;
    background: rgba(0, 0, 0, 0.55);
  }

  &__sheet {
    position: relative;
    background: $bg-panel;
    border-top-left-radius: 32rpx;
    border-top-right-radius: 32rpx;
    padding: 32rpx 32rpx 48rpx;
    max-height: 80vh;
    overflow-y: auto;
    animation: slideUp 0.25s ease;
  }

  &__head {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 24rpx;
  }
  &__title {
    font-size: 30rpx;
    font-weight: 800;
    color: $txt;
  }
  &__close {
    width: 56rpx;
    height: 56rpx;
    border-radius: 50%;
    background: $bg-card;
    color: $txt-2;
    text-align: center;
    line-height: 56rpx;
    font-size: 24rpx;
  }

  &__selected {
    display: flex;
    flex-wrap: wrap;
    gap: 12rpx;
    min-height: 60rpx;
    padding: 16rpx;
    background: $bg-card;
    border-radius: $radius-md;
  }
  &__selected-empty {
    font-size: 22rpx;
    color: $txt-3;
    line-height: 32rpx;
  }

  &__label {
    display: block;
    font-size: 22rpx;
    color: $txt-3;
    letter-spacing: 4rpx;
    margin: 24rpx 0 12rpx;
  }

  &__grid {
    display: flex;
    flex-wrap: wrap;
    gap: 12rpx;
  }

  &__chip {
    display: inline-block;
    padding: 12rpx 24rpx;
    border-radius: 28rpx;
    background: $bg-card;
    border: 1rpx solid $bdr;
    font-size: 22rpx;
    color: $txt-2;
    transition: all 0.2s ease;

    &--active {
      background: rgba(212, 168, 83, 0.1);
      border-color: $gold;
      color: $gold;
    }
    &--disabled {
      opacity: 0.35;
    }
    &--sel {
      padding-right: 18rpx;
    }
    &--sel-like {
      background: rgba(56, 178, 172, 0.12);
      border: 1rpx solid rgba(56, 178, 172, 0.3);
      color: $teal-l;
    }
    &--sel-dislike {
      background: rgba(232, 93, 117, 0.1);
      border: 1rpx solid rgba(232, 93, 117, 0.3);
      color: $red;
    }
  }

  &__input-row {
    display: flex;
    gap: 12rpx;
    align-items: center;
  }
  &__input {
    flex: 1;
    height: 72rpx;
    padding: 0 24rpx;
    background: $bg-card;
    border: 1rpx solid $bdr;
    border-radius: $radius-md;
    font-size: 24rpx;
    color: $txt;
  }
  &__add {
    width: 140rpx;
    height: 72rpx;
    flex-shrink: 0;
    font-size: 22rpx;
  }

  &__actions {
    display: flex;
    gap: 16rpx;
    margin-top: 36rpx;
  }
  &__act {
    flex: 1;
    height: 84rpx;
  }
}

@keyframes slideUp {
  from { transform: translateY(100%); }
  to { transform: translateY(0); }
}
</style>
