# admob_bridge.py - NATIVE ADMOB JAVA BRIDGE
import os
import time

IS_ANDROID = False
try:
    from jnius import autoclass, PythonJavaClass, java_method
    from android.runnable import run_on_ui_thread
    IS_ANDROID = True
except Exception as e:
    IS_ANDROID = False

TEST_REWARDED_ID = "ca-app-pub-3940256099942544/5224354917"

if IS_ANDROID:
    PythonActivity = autoclass('org.kivy.android.PythonActivity')
    AdRequest = autoclass('com.google.android.gms.ads.AdRequest$Builder')
    RewardedAd = autoclass('com.google.android.gms.ads.rewarded.RewardedAd')
    MobileAds = autoclass('com.google.android.gms.ads.MobileAds')

    @run_on_ui_thread
    def init_admob():
        activity = PythonActivity.mActivity
        MobileAds.initialize(activity)

    @run_on_ui_thread
    def load_and_show_rewarded_ad(on_reward_callback):
        try:
            activity = PythonActivity.mActivity
            builder = AdRequest()
            ad_request = builder.build()

            class RewardedCallback(PythonJavaClass):
                __javainterfaces__ = ['com/google/android/gms/ads/rewarded/RewardedAdLoadCallback']
                __javacontext__ = 'app'

                def __init__(self, callback):
                    super().__init__()
                    self.callback = callback

                @java_method('(Lcom/google/android/gms/ads/rewarded/RewardedAd;)V')
                def onAdLoaded(self, rewarded_ad):
                    class ShowCallback(PythonJavaClass):
                        __javainterfaces__ = ['com/google/android/gms/ads/OnUserEarnedRewardListener']
                        __javacontext__ = 'app'

                        def __init__(self, reward_cb):
                            super().__init__()
                            self.reward_cb = reward_cb

                        @java_method('(Lcom/google/android/gms/ads/rewarded/RewardItem;)V')
                        def onUserEarnedReward(self, reward_item):
                            if self.reward_cb:
                                self.reward_cb()

                    rewarded_ad.show(activity, ShowCallback(self.callback))

                @java_method('(Lcom/google/android/gms/ads/LoadAdError;)V')
                def onAdFailedToLoad(self, load_error):
                    print(f"[ADMOB ERROR] {load_error.toString()}")

            RewardedAd.load(activity, TEST_REWARDED_ID, ad_request, RewardedCallback(on_reward_callback))

        except Exception as ex:
            print(f"[ADMOB EXCEPTION] {ex}")

else:
    def init_admob():
        pass

    def load_and_show_rewarded_ad(on_reward_callback):
        if on_reward_callback:
            on_reward_callback()

