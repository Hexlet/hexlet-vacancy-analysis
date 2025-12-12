import Header from "./Header";
import PricingSection from "./PricingSection";
import WhatYouWillGet from "./WhatYouWillGet";
import FrequentlyAskedQuestions from "./FrequentlyAskedQuestions";
import ConsultationBanner from "./ConsultationBanner";

const PricingPage = () => {
 return (
  <>
   <Header />
   <PricingSection/>
   <WhatYouWillGet/>
   <FrequentlyAskedQuestions/>
   <ConsultationBanner />
  </>
 );
};

export default PricingPage;
