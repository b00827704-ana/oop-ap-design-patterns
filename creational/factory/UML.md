\# Factory Pattern – Payment system



```mermaid

classDiagram

&#x20;   class PaymentFactory {

&#x20;       -dict \_processors

&#x20;       +get\_processor(payment\_type) PaymentProcessor

&#x20;       +register\_processor(payment\_type, processor\_class)

&#x20;   }



&#x20;   class PaymentProcessor {

&#x20;       <<abstract>>

&#x20;       +str name

&#x20;       +str error\_message

&#x20;       +validate(details) bool

&#x20;       +process(amount, details) dict

&#x20;   }



&#x20;   class CreditCardProcessor {

&#x20;       +validate(details) bool

&#x20;       +process(amount, details) dict

&#x20;   }

&#x20;   class BankTransferProcessor {

&#x20;       +validate(details) bool

&#x20;       +process(amount, details) dict

&#x20;   }

&#x20;   class PayPalProcessor {

&#x20;       +validate(details) bool

&#x20;       +process(amount, details) dict

&#x20;   }



&#x20;   PaymentFactory ..> PaymentProcessor : creates

&#x20;   PaymentProcessor <|-- CreditCardProcessor

&#x20;   PaymentProcessor <|-- BankTransferProcessor

&#x20;   PaymentProcessor <|-- PayPalProcessor

```

