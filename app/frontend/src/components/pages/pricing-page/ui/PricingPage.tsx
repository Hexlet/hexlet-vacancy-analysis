import { store } from "../../../../store/store";
import { Provider } from "react-redux";
import Header from "./Header";
import PricingSection from "./PricingSection";
import WhatYouWillGet from "./WhatYouWillGet";
import FrequentlyAskedQuestions from "./FrequentlyAskedQuestions";
import ConsultationBanner from "./ConsultationBanner";

const PricingPage = () => {
 return (
  <Provider store={store}>
   <Header />
   <PricingSection />
   <WhatYouWillGet />
   <FrequentlyAskedQuestions />
   <ConsultationBanner />
  </Provider>
 );
};

export default PricingPage;
